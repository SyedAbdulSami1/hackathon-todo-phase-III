"""Base interface for MCP tools in the AI Chatbot feature."""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseMCPTool(ABC):
    """Abstract base class for all MCP tools."""

    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the tool."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """A description of what the tool does."""
        pass

    @property
    @abstractmethod
    def parameters(self) -> Dict[str, Any]:
        """The parameters the tool accepts."""
        pass

    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the tool with the given parameters."""
        pass
