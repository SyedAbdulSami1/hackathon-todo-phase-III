"""Unit tests for the AI Chatbot MCP tools."""

import pytest
from unittest.mock import Mock, MagicMock, patch, AsyncMock
from tools.base import BaseMCPTool
from tools.add_task import AddTaskMCPTool
from tools.update_task import UpdateTaskMCPTool
from tools.delete_task import DeleteTaskMCPTool
from tools.list_tasks import ListTasksMCPTool
from tools.complete_task import CompleteTaskMCPTool


def test_base_mcp_tool_abstract():
    """Test that BaseMCPTool is abstract and raises NotImplementedError."""
    with pytest.raises(TypeError):
        BaseMCPTool()


def test_add_task_tool_properties():
    """Test properties of AddTaskMCPTool."""
    tool = AddTaskMCPTool()
    assert tool.name == "add_task"
    assert "Create" in tool.description
    assert "title" in tool.parameters["required"]


def test_list_tasks_tool_properties():
    """Test properties of ListTasksMCPTool."""
    tool = ListTasksMCPTool()
    assert tool.name == "list_tasks"
    assert "search" in tool.description.lower() or "list" in tool.description.lower()
    assert "status" in tool.parameters["properties"]


def test_update_task_tool_properties():
    """Test properties of UpdateTaskMCPTool."""
    tool = UpdateTaskMCPTool()
    assert tool.name == "update_task"
    assert "Modify" in tool.description or "Update" in tool.description
    assert "task_id" in tool.parameters["required"]


def test_delete_task_tool_properties():
    """Test properties of DeleteTaskMCPTool."""
    tool = DeleteTaskMCPTool()
    assert tool.name == "delete_task"
    assert "Remove" in tool.description or "Delete" in tool.description
    # DeleteTask uses anyOf for requirements
    assert "anyOf" in tool.parameters


def test_complete_task_tool_properties():
    """Test properties of CompleteTaskMCPTool."""
    tool = CompleteTaskMCPTool()
    assert tool.name == "complete_task"
    assert "Mark" in tool.description or "Complete" in tool.description
    assert "task_id" in tool.parameters["required"]


@pytest.mark.asyncio
async def test_tool_registry_execute_tool():
    """Test executing a tool through the registry."""
    with patch("tools.registry.mcp") as mock_mcp:
        # Mock the internal tools dictionary of FastMCP
        mock_tool = MagicMock()
        mock_tool.run = AsyncMock(return_value={"success": True})
        mock_mcp._tool_manager._tools = {"test_tool": mock_tool}
        
        from tools.registry import tool_registry
        result = await tool_registry.execute_tool("test_tool", param="value")
        
        assert result == {"success": True}
        mock_tool.run.assert_called_once_with(arguments={"param": "value"})


def test_tool_registry_get_tool_definitions():
    """Test getting tool definitions from the registry."""
    from tools.registry import tool_registry
    definitions = tool_registry.get_tool_definitions()
    
    assert isinstance(definitions, list)
    # Registry uses FastMCP tools defined in registry.py
    tool_names = [d["function"]["name"] for d in definitions]
    assert "add_task" in tool_names
    assert "list_tasks" in tool_names
