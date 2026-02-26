"""Integration tests for the AI Chatbot chat endpoints."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from uuid import uuid4


def test_post_chat_endpoint_success(test_client, sample_user, db_session):
    """Test successful chat endpoint request."""
    # Add user to database
    sample_user.id = 1
    db_session.add(sample_user)
    db_session.commit()
    db_session.refresh(sample_user)

    # Mock the chat agent
    mock_agent = MagicMock()
    mock_agent.process_request.return_value = {
        "response": "Test response",
        "tool_used": "test_tool",
        "tool_result": {"success": True, "message": "Task created"},
        "actions_taken": ["task_created"],
        "tool_calls": [{"name": "test_tool", "args": {}, "result": {"success": True}}]
    }

    with patch('main.get_chat_agent', return_value=mock_agent):
        response = test_client.post(
            f"/api/{sample_user.id}/chat",
            json={"message": "Create a test task"},
            headers={"Authorization": "Bearer fake_token"}
        )

    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert data["response"] == "Test response"
    assert "conversation_id" in data


def test_post_chat_endpoint_missing_message(test_client, sample_user):
    """Test chat endpoint with missing message."""
    response = test_client.post(
        f"/api/{sample_user.id}/chat",
        json={},
        headers={"Authorization": "Bearer fake_token"}
    )

    assert response.status_code == 422  # Validation error


def test_post_chat_endpoint_invalid_user_id(test_client, sample_user):
    """Test chat endpoint with invalid user ID (mismatch with authenticated user)."""
    # current_user is mocked to be sample_user
    # If we request for a different ID, it should return 403 Forbidden
    response = test_client.post(
        "/api/999/chat",
        json={"message": "Test message"},
        headers={"Authorization": "Bearer fake_token"}
    )

    assert response.status_code == 403


def test_get_user_conversations(test_client, sample_user, db_session):
    """Test getting user conversations."""
    # Add user to database
    sample_user.id = 1
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
    sample_user.id = 1
    db_session.add(sample_user)
    db_session.commit()
    db_session.refresh(sample_user)

    sample_conversation.user_id = str(sample_user.id)
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
    fake_conversation_id = 999

    response = test_client.get(
        f"/api/{sample_user.id}/conversations/{fake_conversation_id}",
        headers={"Authorization": "Bearer fake_token"}
    )

    # Should return 404 for non-existent conversation
    assert response.status_code == 404


def test_get_conversation_history_wrong_user(test_client, sample_user, sample_conversation, db_session):
    """Test getting conversation history for wrong user."""
    # Add user and conversation to database
    sample_user.id = 1
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


def test_post_chat_endpoint_internal_error(test_client, sample_user, db_session):
    """Test chat endpoint with internal server error."""
    # Add user to database
    sample_user.id = 1
    db_session.add(sample_user)
    db_session.commit()

    # Mock the chat agent to raise an exception
    mock_agent = MagicMock()
    mock_agent.process_request.side_effect = Exception("Internal error")

    with patch('main.get_chat_agent', return_value=mock_agent):
        response = test_client.post(
            f"/api/{sample_user.id}/chat",
            json={"message": "Test message"},
            headers={"Authorization": "Bearer fake_token"}
        )

    assert response.status_code == 500
    data = response.json()
    assert "detail" in data
    assert "Internal server error" in data["detail"]


def test_post_chat_endpoint_agent_not_initialized(test_client, sample_user, db_session):
    """Test chat endpoint when agent is not initialized."""
    # Add user to database
    sample_user.id = 1
    db_session.add(sample_user)
    db_session.commit()

    # Mock the chat agent to return None
    with patch('main.get_chat_agent', return_value=None):
        response = test_client.post(
            f"/api/{sample_user.id}/chat",
            json={"message": "Test message"},
            headers={"Authorization": "Bearer fake_token"}
        )

    assert response.status_code == 500
    data = response.json()
    assert "detail" in data
    assert "not initialized" in data["detail"]
