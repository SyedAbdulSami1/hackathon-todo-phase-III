"""Tool binder for connecting the AI agent with MCP tools."""

from typing import Dict, Any
from agents.chat_agent import ChatAgent
from tools.registry import tool_registry


class ToolBinder:
    """Manages the binding of MCP tools to the AI agent."""

    def __init__(self, agent: ChatAgent):
        self.agent = agent
        self.tool_registry = tool_registry

    def bind_tools_to_agent(self):
        """Bind available tools to the agent."""
        # In a real implementation, this would register tools with the AI framework
        # For our implementation, the agent already has access to the tool registry
        pass

    def get_bound_tools_info(self) -> Dict[str, Any]:
        """Get information about tools bound to the agent."""
        tools_info = self.agent.get_available_tools()
        return {
            "tool_count": len(tools_info),
            "tools": tools_info
        }

    def execute_bound_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Execute a bound tool with the given parameters."""
        return self.tool_registry.execute_tool(tool_name, **kwargs)

    def validate_tool_access(self, tool_name: str, user_id: str) -> bool:
        """Validate that a user has access to a particular tool."""
        # For now, all users have access to all tools
        # In a real implementation, this would check user permissions
        return True
