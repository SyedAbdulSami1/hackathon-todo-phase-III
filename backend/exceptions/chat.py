"""Custom exceptions for the chatbot feature."""


class ChatException(Exception):
    """Base exception for chat-related errors."""

    def __init__(self, message: str, error_code: str = "CHAT_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class ConversationNotFoundException(ChatException):
    """Raised when a conversation is not found."""

    def __init__(self, conversation_id: str):
        self.conversation_id = conversation_id
        super().__init__(
            f"Conversation with ID {conversation_id} not found",
            "CONVERSATION_NOT_FOUND"
        )


class MessageNotFoundException(ChatException):
    """Raised when a message is not found."""

    def __init__(self, message_id: str):
        self.message_id = message_id
        super().__init__(
            f"Message with ID {message_id} not found",
            "MESSAGE_NOT_FOUND"
        )


class UnauthorizedAccessException(ChatException):
    """Raised when a user tries to access a resource they don't own."""

    def __init__(self, resource_type: str, resource_id: str):
        self.resource_type = resource_type
        self.resource_id = resource_id
        super().__init__(
            f"Unauthorized access to {resource_type} with ID {resource_id}",
            "UNAUTHORIZED_ACCESS"
        )


class ToolExecutionException(ChatException):
    """Raised when there's an error executing an MCP tool."""

    def __init__(self, tool_name: str, details: str = ""):
        self.tool_name = tool_name
        self.details = details
        message = f"Error executing tool '{tool_name}'"
        if details:
            message += f": {details}"
        super().__init__(message, "TOOL_EXECUTION_ERROR")


class AgentProcessingException(ChatException):
    """Raised when there's an error processing a request with the AI agent."""

    def __init__(self, details: str = ""):
        self.details = details
        message = "Error processing request with AI agent"
        if details:
            message += f": {details}"
        super().__init__(message, "AGENT_PROCESSING_ERROR")


class InvalidRequestException(ChatException):
    """Raised when a request contains invalid data."""

    def __init__(self, field: str, reason: str):
        self.field = field
        self.reason = reason
        super().__init__(
            f"Invalid value for field '{field}': {reason}",
            "INVALID_REQUEST"
        )


class RateLimitExceededException(ChatException):
    """Raised when a user exceeds rate limits."""

    def __init__(self, limit_type: str = "request"):
        self.limit_type = limit_type
        super().__init__(
            f"Rate limit exceeded for {limit_type}",
            "RATE_LIMIT_EXCEEDED"
        )


class DatabaseConnectionException(ChatException):
    """Raised when there's a database connection issue."""

    def __init__(self, details: str = ""):
        self.details = details
        message = "Database connection error"
        if details:
            message += f": {details}"
        super().__init__(message, "DATABASE_CONNECTION_ERROR")
