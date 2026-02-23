"""Registry for MCP tools in the AI Chatbot feature."""

from typing import Dict, List
from tools.base import BaseMCPTool
from tools.todo_create import TodoCreateMCPTool
from tools.todo_update import TodoUpdateMCPTool
from tools.todo_delete import TodoDeleteMCPTool
from tools.todo_search import TodoSearchMCPTool
from tools.todo_complete import TodoCompleteMCPTool


class MCPToolRegistry:
    """Registry to manage all available MCP tools."""

    def __init__(self):
        self._tools: Dict[str, BaseMCPTool] = {}
        self._initialize_tools()

    def _initialize_tools(self):
        """Initialize all available MCP tools."""
        tools = [
            TodoCreateMCPTool(),
            TodoUpdateMCPTool(),
            TodoDeleteMCPTool(),
            TodoSearchMCPTool(),
            TodoCompleteMCPTool()
        ]

        for tool in tools:
            self._tools[tool.name] = tool

    def get_tool(self, name: str) -> BaseMCPTool:
        """Get a tool by name."""
        return self._tools.get(name)

    def get_all_tools(self) -> List[BaseMCPTool]:
        """Get all available tools."""
        return list(self._tools.values())

    def get_tool_names(self) -> List[str]:
        """Get all tool names."""
        return list(self._tools.keys())

    def get_tool_schema(self, name: str) -> dict:
        """Get the schema for a specific tool."""
        tool = self.get_tool(name)
        if tool:
            return {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters
            }
        return None

    def execute_tool(self, name: str, **kwargs) -> dict:
        """Execute a tool with the given parameters."""
        tool = self.get_tool(name)
        if tool:
            return tool.execute(**kwargs)
        else:
            return {
                "success": False,
                "message": f"Tool '{name}' not found"
            }


# Global registry instance
tool_registry = MCPToolRegistry()
