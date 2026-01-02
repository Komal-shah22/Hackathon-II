import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from unittest.mock import MagicMock, patch

from main import app
from mcp_server.handlers import add_task
from mcp_server.schemas import AddTaskInput, AddTaskOutput
from models import Task

client = TestClient(app)

# Mock database session
@pytest.fixture
def mock_db_session():
    db = MagicMock(spec=Session)
    
    def refresh_side_effect(obj):
        obj.id = 1  # Simulate the DB assigning an ID
    
    db.refresh.side_effect = refresh_side_effect
    return db

def test_add_task_handler_success(mock_db_session):
    # Arrange
    input_data = AddTaskInput(title="Buy milk", description="Get some milk from the store")
    user_id = "test_user"

    # We need to patch the get_session used by the handler
    with patch("mcp_server.handlers.get_session") as mock_get_session:
        mock_get_session.return_value.__enter__.return_value = mock_db_session

        # Act
        result = add_task(input_data, user_id=user_id)

    # Assert
    assert isinstance(result, AddTaskOutput)
    assert result.title == "Buy milk"
    assert result.status == "success"
    assert result.task_id == 1
    
    # Check that a task was added to the session
    mock_db_session.add.assert_called_once()
    added_task = mock_db_session.add.call_args[0][0]
    
    assert isinstance(added_task, Task)
    assert added_task.title == "Buy milk"
    assert added_task.description == "Get some milk from the store"
    assert added_task.user_id == user_id
    
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once_with(added_task)