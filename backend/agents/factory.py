"""Factory for creating and managing AI agents."""

from typing import Optional
from backend.agents.config import AgentConfig
from backend.agents.chat_agent import ChatAgent
from backend.agents.tool_binder import ToolBinder


class AgentFactory:
    """Factory class for creating and configuring AI agents."""

    @staticmethod
    def create_chat_agent(config: Optional[AgentConfig] = None) -> ChatAgent:
        """Create a new chat agent with the given configuration."""
        agent_config = config or AgentConfig()
        agent = ChatAgent(agent_config)

        # Bind tools to the agent
        binder = ToolBinder(agent)
        binder.bind_tools_to_agent()

        return agent

    @staticmethod
    def create_default_agent() -> ChatAgent:
        """Create a chat agent with default configuration."""
        return AgentFactory.create_chat_agent()

    @staticmethod
    def get_agent_config() -> AgentConfig:
        """Get the default agent configuration."""
        return AgentConfig()