"""Test for the main application."""

import pytest
from fastapi.testclient import TestClient
from main import app


def test_app_is_created():
    """Test that the FastAPI app is created properly."""
    assert app is not None
    assert hasattr(app, 'routes')


def test_app_has_expected_routes():
    """Test that the app has the expected routes."""
    routes = [route.path for route in app.routes]

    # Check that core routes exist
    assert "/" in routes
    assert "/health" in routes

    # Check that auth and task routes still exist
    assert any("/api/auth" in route for route in app.routes)
    assert any("/api/tasks" in route for route in app.routes)

    # Check that chat routes exist
    assert any("/api/{user_id}/chat" in route for route in app.routes)
    assert any("/api/{user_id}/conversations" in route for route in app.routes)


def test_app_has_correct_tags():
    """Test that routes are tagged correctly."""
    route_tags = []
    for route in app.routes:
        if hasattr(route, 'methods') and hasattr(route, 'tags'):
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
    middleware_types = [type(mw.middleware) for mw in app.user_middleware]
    cors_found = any('CORSMiddleware' in str(mw) for mw in middleware_types)

    assert cors_found, "CORS middleware should be configured"