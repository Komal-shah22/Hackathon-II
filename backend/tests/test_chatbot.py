"""
Tests for the chatbot functionality
"""

import pytest
from fastapi.testclient import TestClient
from main import app
from sqlmodel import create_engine, Session
from db import get_session
from models import User, Task, Conversation, Message
from datetime import datetime
import os


# Override the database URL for testing
TEST_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope="module")
def test_client():
    # Create a test client
    client = TestClient(app)

    # Create test database
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})

    # Create tables
    from models import SQLModel
    SQLModel.metadata.create_all(engine)

    def get_test_session():
        with Session(engine) as session:
            yield session

    # Override the dependency
    app.dependency_overrides[get_session] = get_test_session

    yield client

    # Clean up
    app.dependency_overrides.clear()


def test_models_import_success():
    """Test that our extended models import correctly"""
    from models import User, Task, Conversation, Message, MessageRole

    # Test basic instantiation
    user = User(id="test_user", email="test@example.com", password_hash="hash")
    assert user.email == "test@example.com"

    # Test conversation
    conv = Conversation(user_id="test_user")
    assert conv.user_id == "test_user"

    # Test message
    msg = Message(
        conversation_id=1,
        user_id="test_user",
        role=MessageRole.USER,
        content="Test message"
    )
    assert msg.content == "Test message"
    assert msg.role == MessageRole.USER


def test_schemas_import_success():
    """Test that our extended schemas import correctly"""
    from schemas import ChatRequest, ChatResponse, ToolCall

    # Test basic instantiation
    req = ChatRequest(message="Test message")
    assert req.message == "Test message"

    tool_call = ToolCall(name="test_tool", arguments={"param": "value"})
    assert tool_call.name == "test_tool"

    resp = ChatResponse(conversation_id=1, response="Test response", tool_calls=[])
    assert resp.conversation_id == 1


def test_mcp_tools_service():
    """Test that MCP tools service works correctly"""
    from services.mcp_tools import MCPTaskTools
    from sqlmodel import create_engine, Session
    from models import SQLModel

    # Create in-memory database for testing
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # Create a test user
        test_user = User(id="test_user", email="test@example.com", password_hash="hash")
        session.add(test_user)
        session.commit()

        # Create MCP tools service
        tools = MCPTaskTools(session)

        # Test adding a task
        result = tools.add_task({
            "user_id": "test_user",
            "title": "Test Task",
            "description": "Test Description"
        })

        assert result["status"] == "created"
        assert result["title"] == "Test Task"

        # Test listing tasks
        result = tools.list_tasks({
            "user_id": "test_user",
            "status": "all"
        })

        assert len(result) == 1
        assert result[0]["title"] == "Test Task"

        # Test completing task
        result = tools.complete_task({
            "user_id": "test_user",
            "task_id": result[0]["id"]
        })

        assert result["status"] == "completed"