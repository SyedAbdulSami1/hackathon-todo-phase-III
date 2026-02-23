"""Integration tests for the AI Chatbot chat endpoints."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from uuid import uuid4


def test_post_chat_endpoint_success(test_client, sample_user, db_session):
    """Test successful chat endpoint request."""
    # Add user to database
    db_session.add(sample_user)
    db_session.commit()
    db_session.refresh(sample_user)

    # Mock the chat agent
    mock_agent = MagicMock()
    mock_agent.process_request.return_value = {
        "response": "Test response",
        "tool_used": "test_tool",
        "tool_result": {"success": True, "message": "Task created"},
        "actions_taken": ["task_created"]
    }

    with patch('routers.chat.get_chat_agent', return_value=mock_agent):
        response = test_client.post(
            f"/api/{sample_user.id}/chat",
            json={"message": "Create a test task"},
            headers={"Authorization": "Bearer fake_token"}
        )

    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert data["response"] == "Test response"
    assert data["tool_used"] == "test_tool"


def test_post_chat_endpoint_missing_message(test_client, sample_user):
    """Test chat endpoint with missing message."""
    response = test_client.post(
        f"/api/{sample_user.id}/chat",
        json={},
        headers={"Authorization": "Bearer fake_token"}
    )

    assert response.status_code == 422  # Validation error


def test_post_chat_endpoint_invalid_user_id(test_client):
    """Test chat endpoint with invalid user ID."""
    response = test_client.post(
        "/api/invalid_user_id/chat",
        json={"message": "Test message"},
        headers={"Authorization": "Bearer fake_token"}
    )

    # Should return 400 for invalid user_id
    assert response.status_code == 400


def test_get_user_conversations(test_client, sample_user, db_session):
    """Test getting user conversations."""
    # Add user to database
    db_session.add(sample_user)
    db_session.commit()
    db_session.refresh(sample_user)

    response = test_client.get(
        f"/api/{sample_user.id}/conversations",
        headers={"Authorization": "Bearer fake_token"}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_conversation_history(test_client, sample_user, sample_conversation, db_session):
    """Test getting conversation history."""
    # Add user and conversation to database
    db_session.add(sample_user)
    db_session.commit()
    db_session.refresh(sample_user)

    sample_conversation.user_id = str(sample_user.id) if sample_user.id else "test_user_id"
    db_session.add(sample_conversation)
    db_session.commit()
    db_session.refresh(sample_conversation)

    response = test_client.get(
        f"/api/{sample_user.id}/conversations/{sample_conversation.id}",
        headers={"Authorization": "Bearer fake_token"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "conversation_id" in data
    assert "messages" in data


def test_get_conversation_history_not_found(test_client, sample_user):
    """Test getting non-existent conversation history."""
    fake_conversation_id = str(uuid4())

    response = test_client.get(
        f"/api/{sample_user.id}/conversations/{fake_conversation_id}",
        headers={"Authorization": "Bearer fake_token"}
    )

    # Should return 404 for non-existent conversation
    assert response.status_code == 404


def test_get_conversation_history_wrong_user(test_client, sample_user, sample_conversation, db_session):
    """Test getting conversation history for wrong user."""
    # Add user and conversation to database
    db_session.add(sample_user)
    db_session.commit()
    db_session.refresh(sample_user)

    # Set conversation to a different user
    sample_conversation.user_id = "different_user"
    db_session.add(sample_conversation)
    db_session.commit()
    db_session.refresh(sample_conversation)

    response = test_client.get(
        f"/api/{sample_user.id}/conversations/{sample_conversation.id}",
        headers={"Authorization": "Bearer fake_token"}
    )

    # Should return 404 since conversation doesn't belong to user
    assert response.status_code == 404


def test_post_chat_endpoint_internal_error(test_client, sample_user):
    """Test chat endpoint with internal server error."""
    # Mock the chat agent to raise an exception
    mock_agent = MagicMock()
    mock_agent.process_request.side_effect = Exception("Internal error")

    with patch('routers.chat.get_chat_agent', return_value=mock_agent):
        response = test_client.post(
            f"/api/{sample_user.id}/chat",
            json={"message": "Test message"},
            headers={"Authorization": "Bearer fake_token"}
        )

    assert response.status_code == 500
    data = response.json()
    assert "error" in data


def test_get_user_conversations_internal_error(test_client, sample_user):
    """Test getting user conversations with internal error."""
    # Mock the database query to raise an exception
    with patch('routers.chat.Session') as mock_session_class:
        mock_session = MagicMock()
        mock_session.query.side_effect = Exception("DB error")
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = None

        response = test_client.get(
            f"/api/{sample_user.id}/conversations",
            headers={"Authorization": "Bearer fake_token"}
        )

    assert response.status_code == 500
    data = response.json()
    assert "error" in data


def test_post_chat_endpoint_agent_not_initialized(test_client, sample_user):
    """Test chat endpoint when agent is not initialized."""
    # Mock the chat agent to return None
    with patch('routers.chat.get_chat_agent', return_value=None):
        response = test_client.post(
            f"/api/{sample_user.id}/chat",
            json={"message": "Test message"},
            headers={"Authorization": "Bearer fake_token"}
        )

    assert response.status_code == 500
    data = response.json()
    assert "error" in data
    assert "not initialized" in data["error"]["message"]
