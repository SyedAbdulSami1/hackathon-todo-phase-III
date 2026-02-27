"""Configuration for the AI Chatbot Agent."""

from typing import Dict, Any, Optional
import os


class AgentConfig:
    """Configuration class for the AI agent."""

    def __init__(self):
        self.model_name = os.getenv("AGENT_MODEL_NAME", "gpt-4")
        self.temperature = float(os.getenv("AGENT_TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("AGENT_MAX_TOKENS", "1000"))
        self.api_key = os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
        self.provider = os.getenv("AGENT_PROVIDER", "openai")  # openai, anthropic, etc.

        # Tool configuration
        self.enable_mcp_tools = os.getenv("ENABLE_MCP_TOOLS", "true").lower() == "true"
        self.tool_execution_timeout = int(os.getenv("TOOL_EXECUTION_TIMEOUT", "30"))

        # Memory and context configuration
        self.max_context_length = int(os.getenv("MAX_CONTEXT_LENGTH", "4096"))
        self.max_history_messages = int(os.getenv("MAX_HISTORY_MESSAGES", "20"))

        # Error handling
        self.retry_attempts = int(os.getenv("RETRY_ATTEMPTS", "3"))
        self.fallback_on_error = os.getenv("FALLBACK_ON_ERROR", "true").lower() == "true"

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "model_name": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "provider": self.provider,
            "enable_mcp_tools": self.enable_mcp_tools,
            "tool_execution_timeout": self.tool_execution_timeout,
            "max_context_length": self.max_context_length,
            "max_history_messages": self.max_history_messages,
            "retry_attempts": self.retry_attempts,
            "fallback_on_error": self.fallback_on_error
        }
