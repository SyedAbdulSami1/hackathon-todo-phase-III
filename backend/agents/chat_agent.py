"""AI Chat Agent for processing natural language requests."""

import json
from typing import Dict, Any, List, Optional
from backend.agents.config import AgentConfig
from backend.tools.registry import tool_registry


class ChatAgent:
    """AI agent for processing chat requests and interacting with MCP tools."""

    def __init__(self, config: Optional[AgentConfig] = None):
        self.config = config or AgentConfig()
        self.tools = tool_registry

    def process_request(self, user_input: str, conversation_context: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Process a user's natural language request.

        Args:
            user_input: The user's natural language request
            conversation_context: Previous conversation history

        Returns:
            Dictionary containing the response and any actions taken
        """
        # In a real implementation, we would use an AI service (OpenAI, Anthropic, etc.)
        # For now, we'll simulate the process

        # Parse the user intent (simplified)
        intent = self._parse_intent(user_input)

        if intent and intent.get("needs_tool"):
            # Execute the appropriate tool
            tool_result = self._execute_tool(intent["tool_name"], intent["params"])

            # Generate response based on tool result
            response = self._generate_response_based_on_tool_result(user_input, tool_result)

            return {
                "response": response,
                "tool_used": intent["tool_name"],
                "tool_result": tool_result,
                "actions_taken": [f"{intent['tool_name']} executed"]
            }
        else:
            # Generate a general response
            response = self._generate_general_response(user_input)
            return {
                "response": response,
                "tool_used": None,
                "tool_result": None,
                "actions_taken": ["general response generated"]
            }

    def _parse_intent(self, user_input: str) -> Dict[str, Any]:
        """Parse the user's intent from their input."""
        user_input_lower = user_input.lower()

        # Simple keyword matching for demo purposes
        # In a real implementation, we would use an AI service
        if any(word in user_input_lower for word in ["create", "add", "make", "new"]):
            # Look for task details in the input
            title = self._extract_title(user_input)
            return {
                "needs_tool": True,
                "tool_name": "todo_create_tool",
                "params": {"title": title or "Untitled task"}
            }
        elif any(word in user_input_lower for word in ["update", "change", "modify"]):
            # Look for task ID and updates
            task_id = self._extract_task_id(user_input)
            return {
                "needs_tool": True,
                "tool_name": "todo_update_tool",
                "params": {"task_id": task_id or 1}  # Default to task ID 1 if not found
            }
        elif any(word in user_input_lower for word in ["delete", "remove", "cancel"]):
            # Look for task ID to delete
            task_id = self._extract_task_id(user_input)
            return {
                "needs_tool": True,
                "tool_name": "todo_delete_tool",
                "params": {"task_id": task_id or 1}  # Default to task ID 1 if not found
            }
        elif any(word in user_input_lower for word in ["search", "find", "show", "list", "view"]):
            return {
                "needs_tool": True,
                "tool_name": "todo_search_tool",
                "params": {}
            }
        elif any(word in user_input_lower for word in ["complete", "done", "finish", "mark"]):
            # Check if marking complete or incomplete
            complete = "complete" in user_input_lower or "done" in user_input_lower
            task_id = self._extract_task_id(user_input)
            return {
                "needs_tool": True,
                "tool_name": "todo_complete_tool",
                "params": {
                    "task_id": task_id or 1,  # Default to task ID 1 if not found
                    "complete": complete
                }
            }

        # No specific tool needed
        return {
            "needs_tool": False
        }

    def _extract_title(self, text: str) -> Optional[str]:
        """Extract a potential task title from the input text."""
        # Simple extraction - look for content after action words
        parts = text.split()
        if len(parts) > 1:
            # Skip the first word (likely the action word)
            return " ".join(parts[1:]).strip(".!?")[:200]  # Limit to 200 chars
        return None

    def _extract_task_id(self, text: str) -> Optional[int]:
        """Extract a potential task ID from the input text."""
        # Look for numbers in the text (simple implementation)
        import re
        numbers = re.findall(r'\d+', text)
        if numbers:
            return int(numbers[0])
        return None

    def _execute_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an MCP tool with the given parameters."""
        try:
            # Add user_id to params (would come from request context in real implementation)
            params_with_user = {**params, "user_id": 1}  # Placeholder user_id

            result = self.tools.execute_tool(tool_name, **params_with_user)
            return result
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Error executing tool {tool_name}: {str(e)}"
            }

    def _generate_response_based_on_tool_result(self, user_input: str, tool_result: Dict[str, Any]) -> str:
        """Generate a response based on the tool execution result."""
        if tool_result.get("success"):
            return tool_result.get("message", "Operation completed successfully.")
        else:
            return f"I tried to help with that, but encountered an issue: {tool_result.get('message', 'Unknown error occurred')}"

    def _generate_general_response(self, user_input: str) -> str:
        """Generate a general response for inputs that don't require tools."""
        # In a real implementation, we would use an AI service
        # For now, return a default response
        return f"I understand you said: '{user_input}'. How can I help you with your tasks today?"

    def get_available_tools(self) -> List[Dict[str, Any]]:
        """Get information about all available tools."""
        tools_info = []
        for tool_name in self.tools.get_tool_names():
            schema = self.tools.get_tool_schema(tool_name)
            if schema:
                tools_info.append(schema)
        return tools_info