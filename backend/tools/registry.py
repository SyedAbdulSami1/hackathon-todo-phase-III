"""MCP Tool registry for task operations."""

from typing import Dict, Any, List, Optional
from .base import BaseMCPTool
from .add_task import AddTaskMCPTool
from .list_tasks import ListTasksMCPTool
from .complete_task import CompleteTaskMCPTool
from .delete_task import DeleteTaskMCPTool
from .update_task import UpdateTaskMCPTool

class ToolRegistry:
    """Registry for MCP tools."""

    def __init__(self):
        self._tools: Dict[str, BaseMCPTool] = {}
        self._register_default_tools()

    def _register_default_tools(self):
        """Register all default task tools (Requirement #8)."""
        self.register_tool("add_task", AddTaskMCPTool())
        self.register_tool("list_tasks", ListTasksMCPTool())
        self.register_tool("complete_task", CompleteTaskMCPTool())
        self.register_tool("delete_task", DeleteTaskMCPTool())
        self.register_tool("update_task", UpdateTaskMCPTool())

    def register_tool(self, name: str, tool: BaseMCPTool):
        """Register a new tool."""
        self._tools[name] = tool

    def get_tool(self, name: str) -> Optional[BaseMCPTool]:
        """Get a tool by name."""
        return self._tools.get(name)

    def execute_tool(self, name: str, **kwargs) -> Dict[str, Any]:
        """Execute a tool by name (Stateless DB access)."""
        tool = self.get_tool(name)
        if not tool:
            return {"success": False, "message": f"Tool {name} not found"}
        return tool.execute(**kwargs)

    def get_tool_names(self) -> List[str]:
        """Get all registered tool names."""
        return list(self._tools.keys())

# Global registry instance
tool_registry = ToolRegistry()
