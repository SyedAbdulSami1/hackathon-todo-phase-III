"""Integration tests for the main application."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock


def test_root_endpoint():
    """Test the root endpoint."""
    from main import app
    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "RELOADED" in data["message"]


def test_health_check_endpoint():
    """Test the health check endpoint."""
    from main import app
    client = TestClient(app)

    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"


def test_chat_route_registered():
    """Test that chat routes are registered."""
    from main import app

    # Check if chat routes are included
    routes = [route.path for route in app.routes]
    assert any("/api/{user_id}/chat" in route for route in routes)
    assert any("/api/{user_id}/conversations" in route for route in routes)


def test_main_app_lifespan():
    """Test that the app lifespan initializes the chat agent."""
    # This test verifies that the lifespan function works correctly
    from main import app, get_chat_agent
    from fastapi.testclient import TestClient

    with TestClient(app) as client:
        # Make a request to trigger the lifespan startup
        client.get("/health")

        # Check if the agent is initialized
        agent = get_chat_agent()
        assert agent is not None


def test_main_app_lifespan_with_mocked_agent():
    """Test the app lifespan with a mocked agent."""
    from main import app
    from fastapi.testclient import TestClient

    with patch('main.AgentFactory') as mock_agent_factory:
        mock_agent = MagicMock()
        mock_agent_factory.create_default_agent.return_value = mock_agent

        with TestClient(app) as client:
            client.get("/health")

        # Verify that the agent factory was called
        mock_agent_factory.create_default_agent.assert_called_once()


def test_auth_routes_still_work():
    """Test that existing auth routes still work after adding chat routes."""
    from main import app
    client = TestClient(app)

    # Test that auth routes are still accessible
    # Note: These might fail due to missing dependencies, but they should be registered
    routes = [route.path for route in app.routes]
    auth_routes_exist = any("/api/auth" in route for route in routes)
    tasks_routes_exist = any("/api/tasks" in route for route in routes)

    assert auth_routes_exist, "Auth routes should still be registered"
    assert tasks_routes_exist, "Task routes should still be registered"
