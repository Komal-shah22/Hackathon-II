import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch, AsyncMock
from main import app
from models import Task, Conversation, Message
from sqlmodel import Session
import os
from routes.chat import get_openai_client, get_openai_tool_definitions
from auth import get_current_user_id
from mcp_server.schemas import (
    ListTasksInput, ListTasksOutput, TaskListItem,
    CompleteTaskInput, CompleteTaskOutput,
    DeleteTaskInput, DeleteTaskOutput,
    UpdateTaskInput, UpdateTaskOutput
)

client = TestClient(app)


@pytest.fixture
def mock_openai_client():
    mock_client_instance = AsyncMock()

    # Setup mock responses
    mock_assistant = MagicMock()
    mock_assistant.id = "asst_123"
    mock_client_instance.beta.assistants.create.return_value = mock_assistant

    mock_thread = MagicMock()
    mock_thread.id = "thread_123"
    mock_client_instance.beta.threads.create.return_value = mock_thread

    mock_client_instance.beta.threads.messages.create.return_value = MagicMock()

    mock_run = MagicMock()
    mock_run.id = "run_123"
    mock_run.status = "requires_action"

    mock_tool_call = MagicMock()
    mock_tool_call.id = "call_123"
    mock_tool_call.function.name = "add_task"
    mock_tool_call.function.arguments = '{"title": "buy milk"}'

    mock_required_action = MagicMock()
    mock_required_action.submit_tool_outputs.tool_calls = [mock_tool_call]
    mock_run.required_action = mock_required_action

    mock_client_instance.beta.threads.runs.create.return_value = mock_run

    # Mock the run retrieval
    mock_in_progress_run = MagicMock(status="in_progress")
    mock_completed_run = MagicMock(status="completed")
    mock_client_instance.beta.threads.runs.retrieve.side_effect = [
        mock_in_progress_run,
        mock_completed_run
    ]

    mock_client_instance.beta.threads.runs.submit_tool_outputs.return_value = mock_in_progress_run

    # Mock the final messages list
    mock_message_list = MagicMock()
    mock_assistant_message = MagicMock()
    mock_assistant_message.role = "assistant"
    mock_assistant_message.content = [MagicMock(text=MagicMock(value="I have added the task to buy milk."))]
    mock_message_list.data = [mock_assistant_message]
    mock_client_instance.beta.threads.messages.list.return_value = mock_message_list

    yield mock_client_instance


@pytest.fixture
def override_get_openai_client(mock_openai_client):
    app.dependency_overrides[get_openai_client] = lambda: mock_openai_client
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def mock_db_session():
    db = MagicMock(spec=Session)
    def refresh_side_effect(obj):
        if hasattr(obj, 'id') and obj.id is None:
            obj.id = 1
    db.refresh.side_effect = refresh_side_effect
    return db


@pytest.fixture
def override_get_current_user_id():
    app.dependency_overrides[get_current_user_id] = lambda: "test_user"
    yield
    app.dependency_overrides.clear()


# ============== T011: Integration test for /chat endpoint ==============

def test_chat_endpoint_with_tool_call(
    mock_db_session,
    override_get_current_user_id,
    override_get_openai_client
):
    """
    T011: Integration test for /chat endpoint with task creation intent.
    Verifies that sending "Add a task to buy milk" creates the task.
    """
    user_id = "test_user"
    request_data = {"message": "Add a task to buy milk"}

    with patch("mcp_server.handlers.get_session") as mock_get_session:
        mock_get_session.return_value.__enter__.return_value = mock_db_session

        # Act
        response = client.post(f"/api/{user_id}/chat", json=request_data)

    # Assert
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["response"] == "I have added the task to buy milk."
    assert "conversation_id" in response_json
    assert response_json["conversation_id"] == 1

    # Verify that the add_task tool was called which results in a DB commit
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()

    # Verify the task content
    added_task = mock_db_session.add.call_args[0][0]
    assert isinstance(added_task, Task)
    assert added_task.title == "buy milk"
    assert added_task.user_id == user_id


def test_chat_endpoint_new_conversation(
    mock_db_session,
    override_get_current_user_id,
    override_get_openai_client
):
    """
    T011: Integration test for creating a new conversation.
    """
    user_id = "test_user"
    request_data = {"message": "Add a task to buy milk"}

    with patch("mcp_server.handlers.get_session") as mock_get_session:
        mock_get_session.return_value.__enter__.return_value = mock_db_session

        # Act
        response = client.post(f"/api/{user_id}/chat", json=request_data)

    # Assert
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["conversation_id"] == 1


def test_chat_endpoint_continues_conversation(
    mock_db_session,
    override_get_current_user_id,
    override_get_openai_client
):
    """
    T011: Integration test for continuing an existing conversation.
    """
    user_id = "test_user"
    request_data = {
        "message": "What are my tasks?",
        "conversation_id": 1
    }

    with patch("mcp_server.handlers.get_session") as mock_get_session:
        mock_get_session.return_value.__enter__.return_value = mock_db_session

        # Act
        response = client.post(f"/api/{user_id}/chat", json=request_data)

    # Assert
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["conversation_id"] == 1


def test_chat_endpoint_forbidden_user_id_mismatch(
    mock_db_session,
    override_get_current_user_id
):
    """
    T011: Integration test verifying user_id in path must match JWT.
    """
    request_data = {"message": "Add a task"}

    # Act - user_id in path is "other_user" but JWT says "test_user"
    response = client.post(f"/api/other_user/chat", json=request_data)

    # Assert
    assert response.status_code == 403
    assert response.json()["detail"] == "Forbidden"


# ============== T018: Unit tests for list_tasks, complete_task, delete_task, update_task ==============

def test_list_tasks_handler_all(mock_db_session):
    """T018: Test list_tasks handler returns all tasks when no filters."""
    from mcp_server.handlers import list_tasks
    from mcp_server.schemas import ListTasksInput

    input_data = ListTasksInput()
    user_id = "test_user"

    # Create mock tasks
    mock_task1 = MagicMock(spec=Task)
    mock_task1.id = 1
    mock_task1.title = "Task 1"
    mock_task1.description = "Description 1"
    mock_task1.completed = False
    mock_task1.priority = None
    mock_task1.category = None
    mock_task1.due_date = None
    mock_task1.created_at = MagicMock()

    mock_task2 = MagicMock(spec=Task)
    mock_task2.id = 2
    mock_task2.title = "Task 2"
    mock_task2.description = None
    mock_task2.completed = True
    mock_task2.priority = None
    mock_task2.category = None
    mock_task2.due_date = None
    mock_task2.created_at = MagicMock()

    def exec_side_effect(statement):
        return MagicMock(all=MagicMock(return_value=[mock_task1, mock_task2]))

    mock_db_session.exec.side_effect = exec_side_effect

    with patch("mcp_server.handlers.get_session") as mock_get_session:
        mock_get_session.return_value.__enter__.return_value = mock_db_session

        result = list_tasks(input_data, user_id=user_id)

    assert isinstance(result, ListTasksOutput)
    assert result.total_count == 2
    assert len(result.tasks) == 2
    assert result.status == "success"


def test_list_tasks_handler_filter_pending(mock_db_session):
    """T018: Test list_tasks handler filters pending tasks."""
    from mcp_server.handlers import list_tasks
    from mcp_server.schemas import ListTasksInput

    input_data = ListTasksInput(status="pending")
    user_id = "test_user"

    mock_task = MagicMock(spec=Task)
    mock_task.id = 1
    mock_task.title = "Pending Task"
    mock_task.description = None
    mock_task.completed = False
    mock_task.priority = None
    mock_task.category = None
    mock_task.due_date = None
    mock_task.created_at = MagicMock()

    def exec_side_effect(statement):
        return MagicMock(all=MagicMock(return_value=[mock_task]))

    mock_db_session.exec.side_effect = exec_side_effect

    with patch("mcp_server.handlers.get_session") as mock_get_session:
        mock_get_session.return_value.__enter__.return_value = mock_db_session

        result = list_tasks(input_data, user_id=user_id)

    assert isinstance(result, ListTasksOutput)
    assert result.total_count == 1
    assert result.tasks[0].completed == False


def test_complete_task_handler_success(mock_db_session):
    """T018: Test complete_task handler marks task as complete."""
    from mcp_server.handlers import complete_task
    from mcp_server.schemas import CompleteTaskInput

    input_data = CompleteTaskInput(task_id=1)
    user_id = "test_user"

    mock_task = MagicMock(spec=Task)
    mock_task.id = 1
    mock_task.title = "Test Task"
    mock_task.completed = False
    mock_task.user_id = user_id

    mock_db_session.get.return_value = mock_task

    with patch("mcp_server.handlers.get_session") as mock_get_session:
        mock_get_session.return_value.__enter__.return_value = mock_db_session

        result = complete_task(input_data, user_id=user_id)

    assert isinstance(result, CompleteTaskOutput)
    assert result.task_id == 1
    assert result.completed == True
    assert result.title == "Test Task"
    mock_db_session.commit.assert_called_once()


def test_complete_task_handler_not_found(mock_db_session):
    """T018: Test complete_task handler raises error for non-existent task."""
    from mcp_server.handlers import complete_task
    from mcp_server.schemas import CompleteTaskInput

    input_data = CompleteTaskInput(task_id=999)
    user_id = "test_user"

    mock_db_session.get.return_value = None

    with patch("mcp_server.handlers.get_session") as mock_get_session:
        mock_get_session.return_value.__enter__.return_value = mock_db_session

        with pytest.raises(ValueError, match="Task with ID 999 not found"):
            complete_task(input_data, user_id=user_id)


def test_complete_task_handler_forbidden(mock_db_session):
    """T018: Test complete_task handler raises error for task owned by another user."""
    from mcp_server.handlers import complete_task
    from mcp_server.schemas import CompleteTaskInput

    input_data = CompleteTaskInput(task_id=1)
    user_id = "test_user"

    mock_task = MagicMock(spec=Task)
    mock_task.id = 1
    mock_task.user_id = "other_user"  # Different owner

    mock_db_session.get.return_value = mock_task

    with patch("mcp_server.handlers.get_session") as mock_get_session:
        mock_get_session.return_value.__enter__.return_value = mock_db_session

        with pytest.raises(PermissionError, match="do not have permission"):
            complete_task(input_data, user_id=user_id)


def test_delete_task_handler_success(mock_db_session):
    """T018: Test delete_task handler removes task."""
    from mcp_server.handlers import delete_task
    from mcp_server.schemas import DeleteTaskInput

    input_data = DeleteTaskInput(task_id=1)
    user_id = "test_user"

    mock_task = MagicMock(spec=Task)
    mock_task.id = 1
    mock_task.title = "Test Task"
    mock_task.user_id = user_id

    mock_db_session.get.return_value = mock_task

    with patch("mcp_server.handlers.get_session") as mock_get_session:
        mock_get_session.return_value.__enter__.return_value = mock_db_session

        result = delete_task(input_data, user_id=user_id)

    assert isinstance(result, DeleteTaskOutput)
    assert result.task_id == 1
    assert result.title == "Test Task"
    mock_db_session.delete.assert_called_once_with(mock_task)
    mock_db_session.commit.assert_called_once()


def test_delete_task_handler_not_found(mock_db_session):
    """T018: Test delete_task handler raises error for non-existent task."""
    from mcp_server.handlers import delete_task
    from mcp_server.schemas import DeleteTaskInput

    input_data = DeleteTaskInput(task_id=999)
    user_id = "test_user"

    mock_db_session.get.return_value = None

    with patch("mcp_server.handlers.get_session") as mock_get_session:
        mock_get_session.return_value.__enter__.return_value = mock_db_session

        with pytest.raises(ValueError, match="Task with ID 999 not found"):
            delete_task(input_data, user_id=user_id)


def test_update_task_handler_success(mock_db_session):
    """T018: Test update_task handler modifies task details."""
    from mcp_server.handlers import update_task
    from mcp_server.schemas import UpdateTaskInput

    input_data = UpdateTaskInput(task_id=1, title="Updated Title", description="New description")
    user_id = "test_user"

    mock_task = MagicMock(spec=Task)
    mock_task.id = 1
    mock_task.title = "Original Title"
    mock_task.description = None
    mock_task.priority = None
    mock_task.category = None
    mock_task.user_id = user_id

    mock_db_session.get.return_value = mock_task

    with patch("mcp_server.handlers.get_session") as mock_get_session:
        mock_get_session.return_value.__enter__.return_value = mock_db_session

        result = update_task(input_data, user_id=user_id)

    assert isinstance(result, UpdateTaskOutput)
    assert result.task_id == 1
    assert result.title == "Updated Title"
    assert result.description == "New description"
    mock_db_session.commit.assert_called_once()


# ============== T025: Integration test for conversation retrieval and context-aware turn ==============

def test_get_messages_endpoint(
    mock_db_session,
    override_get_current_user_id
):
    """
    T025: Integration test for conversation message retrieval.
    Verifies that messages can be retrieved for a conversation.
    """
    user_id = "test_user"

    # Create mock conversation
    mock_conversation = MagicMock()
    mock_conversation.id = 1
    mock_conversation.user_id = user_id

    # Create mock messages
    mock_message1 = MagicMock()
    mock_message1.id = 1
    mock_message1.conversation_id = 1
    mock_message1.role = "user"
    mock_message1.content = "Add a task"
    mock_message1.created_at = MagicMock()
    mock_message1.created_at.isoformat.return_value = "2025-01-01T10:00:00"

    mock_message2 = MagicMock()
    mock_message2.id = 2
    mock_message2.conversation_id = 1
    mock_message2.role = "assistant"
    mock_message2.content = "I have added your task."
    mock_message2.created_at = MagicMock()
    mock_message2.created_at.isoformat.return_value = "2025-01-01T10:00:01"

    def exec_side_effect(statement):
        if "Conversation" in str(statement):
            return MagicMock(first=MagicMock(return_value=mock_conversation))
        else:
            return MagicMock(all=MagicMock(return_value=[mock_message1, mock_message2]))

    mock_db_session.exec.side_effect = exec_side_effect

    with patch("routes.chat.get_session") as mock_get_session:
        mock_get_session.return_value.__enter__.return_value = mock_db_session

        # Act
        response = client.get(f"/api/{user_id}/chat/1/messages")

    # Assert
    assert response.status_code == 200
    messages = response.json()
    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "Add a task"
    assert messages[1]["role"] == "assistant"
    assert messages[1]["content"] == "I have added your task."


def test_list_conversations_endpoint(
    mock_db_session,
    override_get_current_user_id
):
    """
    T025: Integration test for listing user conversations.
    """
    user_id = "test_user"

    # Create mock conversations
    mock_conversation = MagicMock()
    mock_conversation.id = 1
    mock_conversation.updated_at = MagicMock()
    mock_conversation.updated_at.isoformat.return_value = "2025-01-01T10:00:00"

    def exec_side_effect(statement):
        if "Conversation" in str(statement):
            return MagicMock(all=MagicMock(return_value=[mock_conversation]))
        else:
            return MagicMock(all=MagicMock(return_value=[]))

    mock_db_session.exec.side_effect = exec_side_effect

    with patch("routes.chat.get_session") as mock_get_session:
        mock_get_session.return_value.__enter__.return_value = mock_db_session

        # Act
        response = client.get(f"/api/{user_id}/chat/conversations")

    # Assert
    assert response.status_code == 200
    conversations = response.json()
    assert len(conversations) == 1
    assert conversations[0]["id"] == 1


def test_get_messages_conversation_not_found(
    mock_db_session,
    override_get_current_user_id
):
    """
    T025: Integration test for 404 when conversation not found.
    """
    user_id = "test_user"

    def exec_side_effect(statement):
        return MagicMock(first=MagicMock(return_value=None))

    mock_db_session.exec.side_effect = exec_side_effect

    with patch("routes.chat.get_session") as mock_get_session:
        mock_get_session.return_value.__enter__.return_value = mock_db_session

        # Act
        response = client.get(f"/api/{user_id}/chat/999/messages")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Conversation not found"
