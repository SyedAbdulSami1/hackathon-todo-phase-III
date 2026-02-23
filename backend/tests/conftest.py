"""Test configuration and fixtures for the AI Chatbot project."""

import pytest
import tempfile
import os
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session
from sqlmodel.pool import StaticPool

from main import app
from db import SQLModel, engine, get_session
from models.user import User
from models.conversation import Conversation
from models.message import Message


@pytest.fixture(scope="function")
def db_engine():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(bind=engine)
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(db_engine):
    """Create a database session for testing."""
    with Session(db_engine) as session:
        yield session


@pytest.fixture(scope="function")
def override_get_session(db_session):
    """Override the get_session dependency to use the test session."""
    def _get_session():
        return db_session

    app.dependency_overrides[get_session] = _get_session
    yield db_session
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_client(override_get_session):
    """Create a test client with overridden dependencies."""
    with TestClient(app) as client:
        yield client


@pytest.fixture
def mock_agent():
    """Mock chat agent for testing."""
    agent = MagicMock()
    agent.process_request.return_value = {
        "response": "Test response",
        "tool_used": "test_tool",
        "tool_result": {"success": True},
        "actions_taken": ["test_action"]
    }
    return agent


@pytest.fixture
def sample_user():
    """Sample user for testing."""
    return User(
        username="testuser",
        email="test@example.com",
        hashed_password="fake_hashed_password"
    )


@pytest.fixture
def sample_conversation(sample_user):
    """Sample conversation for testing."""
    return Conversation(
        user_id=sample_user.id if sample_user.id else "test_user_id",
        title="Test Conversation"
    )


@pytest.fixture
def sample_message(sample_conversation):
    """Sample message for testing."""
    return Message(
        conversation_id=sample_conversation.id,
        sender_type="user",
        content="Test message content"
    )
