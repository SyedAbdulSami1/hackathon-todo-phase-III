"""Error handler for MCP tool executions."""


class MCPErrorHandler:
    """Handler for MCP tool execution errors."""

    @staticmethod
    def handle_tool_error(tool_name: str, error: Exception) -> dict:
        """
        Handle an error that occurred during MCP tool execution.

        Args:
            tool_name: The name of the tool that failed
            error: The error that occurred

        Returns:
            Dictionary with error details
        """
        error_details = {
            "success": False,
            "tool_name": tool_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "fallback_message": f"I encountered an issue with the {tool_name} tool. Please try rephrasing your request."
        }

        # Log the error (in a real implementation)
        print(f"MCP Tool Error - Tool: {tool_name}, Error: {str(error)}")

        return error_details

    @staticmethod
    def handle_validation_error(tool_name: str, param_name: str, value: any, expected_type: str) -> dict:
        """
        Handle a validation error for MCP tool parameters.

        Args:
            tool_name: The name of the tool with validation error
            param_name: The name of the parameter that failed validation
            value: The invalid value
            expected_type: The expected type

        Returns:
            Dictionary with validation error details
        """
        error_details = {
            "success": False,
            "tool_name": tool_name,
            "error_type": "validation_error",
            "error_message": f"Invalid value for parameter '{param_name}': Expected {expected_type}, got {type(value).__name__}",
            "param_name": param_name,
            "expected_type": expected_type,
            "actual_value": str(value),
            "fallback_message": f"The input for {param_name} wasn't in the expected format for the {tool_name} tool."
        }

        return error_details

    @staticmethod
    def handle_timeout_error(tool_name: str, timeout_duration: int) -> dict:
        """
        Handle a timeout error for MCP tool execution.

        Args:
            tool_name: The name of the tool that timed out
            timeout_duration: The timeout duration in seconds

        Returns:
            Dictionary with timeout error details
        """
        error_details = {
            "success": False,
            "tool_name": tool_name,
            "error_type": "timeout_error",
            "error_message": f"Tool {tool_name} timed out after {timeout_duration} seconds",
            "timeout_duration": timeout_duration,
            "fallback_message": f"The {tool_name} tool took too long to respond. Please try again or rephrase your request."
        }

        return error_details

    @staticmethod
    def handle_permission_error(tool_name: str, user_id: str) -> dict:
        """
        Handle a permission error for MCP tool execution.

        Args:
            tool_name: The name of the tool that access was denied for
            user_id: The ID of the user who lacks permission

        Returns:
            Dictionary with permission error details
        """
        error_details = {
            "success": False,
            "tool_name": tool_name,
            "error_type": "permission_error",
            "error_message": f"User {user_id} does not have permission to use tool {tool_name}",
            "user_id": user_id,
            "fallback_message": f"You don't have permission to use the {tool_name} tool."
        }

        return error_details

    @staticmethod
    def create_fallback_response(original_request: dict, error_details: dict) -> dict:
        """
        Create a fallback response when a tool fails.

        Args:
            original_request: The original request that led to the error
            error_details: The details of the error that occurred

        Returns:
            Dictionary with fallback response
        """
        return {
            "success": False,
            "original_request": original_request,
            "error_details": error_details,
            "suggestion": "I couldn't complete that action. Could you try rephrasing your request?",
            "available_alternatives": [
                "Try a simpler request",
                "Be more specific about what you want",
                "Ask for help with a different task"
            ]
        }

    @staticmethod
    def should_retry(error_type: str, attempt_number: int, max_attempts: int) -> bool:
        """
        Determine if an operation should be retried based on the error type.

        Args:
            error_type: The type of error that occurred
            attempt_number: The current attempt number
            max_attempts: The maximum number of attempts

        Returns:
            Boolean indicating if the operation should be retried
        """
        # Don't retry on validation errors or permission errors
        non_retryable_errors = ["validation_error", "permission_error"]

        if error_type in non_retryable_errors:
            return False

        # Retry other errors up to the max attempts
        return attempt_number < max_attempts
