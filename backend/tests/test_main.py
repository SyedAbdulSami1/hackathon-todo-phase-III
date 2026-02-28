"""Comprehensive tests for the main application."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from index import app, get_chat_agent
from starlette.routing import Route


def test_app_is_created():
    """Test that the FastAPI app is created properly."""
    assert app is not None
    assert hasattr(app, 'routes')


def test_root_endpoint():
    """Test the root endpoint."""
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_health_check_endpoint():
    """Test the health check endpoint."""
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"


def test_app_has_expected_routes():
    """Test that the app has the expected routes."""
    routes = [route.path for route in app.routes if isinstance(route, Route)]

    # Check that core routes exist
    assert "/" in routes
    assert "/health" in routes

    # Check that auth and task routes still exist
    assert any("/api/auth" in path for path in routes)
    assert any("/api/tasks" in path for path in routes)

    # Check that chat routes exist
    assert any("/api/{user_id}/chat" in path for path in routes)
    assert any("/api/{user_id}/conversations" in path for path in routes)


def test_app_has_correct_tags():
    """Test that routes are tagged correctly."""
    route_tags = []
    for route in app.routes:
        if isinstance(route, Route) and hasattr(route, 'tags'):
            route_tags.extend(route.tags or [])

    # Ensure auth and tasks tags still exist
    assert "auth" in route_tags
    assert "tasks" in route_tags
    assert "chat" in route_tags


def test_openapi_schema():
    """Test that the OpenAPI schema is generated properly."""
    client = TestClient(app)
    response = client.get("/openapi.json")
    assert response.status_code == 200

    schema = response.json()
    assert "openapi" in schema
    assert "info" in schema
    assert "paths" in schema

    # Verify that our new chat endpoints are in the schema
    paths = schema["paths"]
    assert any("/{user_id}/chat" in path for path in paths)
    assert any("/{user_id}/conversations" in path for path in paths)


def test_cors_middleware():
    """Test that CORS middleware is configured."""
    # Check if CORS middleware is in the app's middleware stack
    # In newer FastAPI versions, we can check the app.user_middleware or app.middleware_stack
    cors_found = False
    for middleware in app.user_middleware:
        if "CORSMiddleware" in str(middleware.cls):
            cors_found = True
            break

    assert cors_found, "CORS middleware should be configured"


def test_main_app_lifespan():
    """Test that the app lifespan initializes the chat agent."""
    with TestClient(app) as client:
        # Make a request to trigger the lifespan startup
        client.get("/health")

        # Check if the agent is initialized
        agent = get_chat_agent()
        assert agent is not None


def test_main_app_lifespan_with_mocked_agent():
    """Test the app lifespan with a mocked agent."""
    with patch('index.AgentFactory') as mock_agent_factory:
        mock_agent = MagicMock()
        mock_agent_factory.create_default_agent.return_value = mock_agent

        # Clear app state for testing lifespan if possible
        # We can't easily clear the global chat_agent in main.py without direct access
        # but the patch should catch the call.
        
        with TestClient(app) as client:
            client.get("/health")

        # Verify that the agent factory was called
        mock_agent_factory.create_default_agent.assert_called_once()
