"""Unit tests for the AI Chatbot MCP tools."""

import pytest
from unittest.mock import Mock, MagicMock
from tools.base import BaseMCPTool
from tools.todo_create import TodoCreateMCPTool
from tools.todo_update import TodoUpdateMCPTool
from tools.todo_delete import TodoDeleteMCPTool
from tools.todo_search import TodoSearchMCPTool
from tools.todo_complete import TodoCompleteMCPTool
from tools.registry import MCPToolRegistry


def test_base_mcp_tool_abstract():
    """Test that BaseMCPTool is abstract and raises NotImplementedError."""
    with pytest.raises(TypeError):
        BaseMCPTool()


def test_todo_create_tool_properties():
    """Test TodoCreateMCPTool properties."""
    tool = TodoCreateMCPTool()

    assert tool.name == "todo_create_tool"
    assert "Create a new todo task" in tool.description
    assert "title" in tool.parameters["properties"]
    assert "title" in tool.parameters["required"]


def test_todo_create_tool_execute_success(mocker):
    """Test TodoCreateMCPTool execute method."""
    # Mock the database session
    mock_session = Mock()
    mock_task = Mock()
    mock_task.id = 1
    mock_session.add = Mock()
    mock_session.commit = Mock()
    mock_session.refresh = Mock(return_value=mock_task)

    # Patch the Session context manager
    mocker.patch('tools.todo_create.Session', return_value=mock_session.__enter__)
    mocker.patch.object(mock_session, '__enter__', return_value=mock_session)
    mocker.patch.object(mock_session, '__exit__', return_value=None)

    tool = TodoCreateMCPTool()
    result = tool.execute(title="Test Task", description="Test Description", user_id=1)

    assert result["success"] is True
    assert result["task_id"] == 1
    assert "created successfully" in result["message"]


def test_todo_update_tool_properties():
    """Test TodoUpdateMCPTool properties."""
    tool = TodoUpdateMCPTool()

    assert tool.name == "todo_update_tool"
    assert "Update an existing todo task" in tool.description
    assert "task_id" in tool.parameters["properties"]
    assert "task_id" in tool.parameters["required"]


def test_todo_delete_tool_properties():
    """Test TodoDeleteMCPTool properties."""
    tool = TodoDeleteMCPTool()

    assert tool.name == "todo_delete_tool"
    assert "Delete a todo task" in tool.description
    assert "task_id" in tool.parameters["properties"] or "title" in tool.parameters["properties"]


def test_todo_search_tool_properties():
    """Test TodoSearchMCPTool properties."""
    tool = TodoSearchMCPTool()

    assert tool.name == "todo_search_tool"
    assert "Search for existing tasks" in tool.description
    assert "status" in tool.parameters["properties"]


def test_todo_complete_tool_properties():
    """Test TodoCompleteMCPTool properties."""
    tool = TodoCompleteMCPTool()

    assert tool.name == "todo_complete_tool"
    assert "Mark a task as complete" in tool.description
    assert "task_id" in tool.parameters["properties"]
    assert "complete" in tool.parameters["properties"]
    assert "task_id" in tool.parameters["required"]
    assert "complete" in tool.parameters["required"]


def test_mcp_tool_registry_initialization():
    """Test MCPToolRegistry initialization."""
    registry = MCPToolRegistry()

    assert len(registry.get_all_tools()) == 5  # 5 tools registered
    assert "todo_create_tool" in registry.get_tool_names()
    assert "todo_update_tool" in registry.get_tool_names()
    assert "todo_delete_tool" in registry.get_tool_names()
    assert "todo_search_tool" in registry.get_tool_names()
    assert "todo_complete_tool" in registry.get_tool_names()


def test_mcp_tool_registry_get_tool():
    """Test MCPToolRegistry get_tool method."""
    registry = MCPToolRegistry()

    tool = registry.get_tool("todo_create_tool")
    assert tool is not None
    assert tool.name == "todo_create_tool"

    nonexistent_tool = registry.get_tool("nonexistent_tool")
    assert nonexistent_tool is None


def test_mcp_tool_registry_execute_tool():
    """Test MCPToolRegistry execute_tool method."""
    registry = MCPToolRegistry()

    # Mock the tool execution
    result = registry.execute_tool("nonexistent_tool")
    assert result["success"] is False
    assert "not found" in result["message"]


def test_mcp_tool_registry_tool_schema():
    """Test MCPToolRegistry get_tool_schema method."""
    registry = MCPToolRegistry()

    schema = registry.get_tool_schema("todo_create_tool")
    assert schema is not None
    assert schema["name"] == "todo_create_tool"
    assert "description" in schema
    assert "parameters" in schema

    nonexistent_schema = registry.get_tool_schema("nonexistent_tool")
    assert nonexistent_schema is None