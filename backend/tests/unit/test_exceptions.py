"""Unit tests for the AI Chatbot exceptions."""

import pytest
from exceptions.chat import (
    ChatException,
    ConversationNotFoundException,
    MessageNotFoundException,
    UnauthorizedAccessException,
    ToolExecutionException,
    AgentProcessingException,
    InvalidRequestException,
    RateLimitExceededException,
    DatabaseConnectionException
)


def test_chat_exception_base():
    """Test ChatException base class."""
    exception = ChatException("Test message")

    assert str(exception) == "Test message"
    assert exception.message == "Test message"
    assert exception.error_code == "CHAT_ERROR"


def test_chat_exception_custom_error_code():
    """Test ChatException with custom error code."""
    exception = ChatException("Test message", "CUSTOM_CODE")

    assert str(exception) == "Test message"
    assert exception.message == "Test message"
    assert exception.error_code == "CUSTOM_CODE"


def test_conversation_not_found_exception():
    """Test ConversationNotFoundException."""
    exception = ConversationNotFoundException("conv_123")

    assert "conv_123" in str(exception)
    assert exception.conversation_id == "conv_123"
    assert exception.error_code == "CONVERSATION_NOT_FOUND"


def test_message_not_found_exception():
    """Test MessageNotFoundException."""
    exception = MessageNotFoundException("msg_123")

    assert "msg_123" in str(exception)
    assert exception.message_id == "msg_123"
    assert exception.error_code == "MESSAGE_NOT_FOUND"


def test_unauthorized_access_exception():
    """Test UnauthorizedAccessException."""
    exception = UnauthorizedAccessException("conversation", "conv_123")

    assert "conversation" in str(exception)
    assert "conv_123" in str(exception)
    assert exception.resource_type == "conversation"
    assert exception.resource_id == "conv_123"
    assert exception.error_code == "UNAUTHORIZED_ACCESS"


def test_tool_execution_exception():
    """Test ToolExecutionException."""
    exception = ToolExecutionException("test_tool", "Test details")

    assert "test_tool" in str(exception)
    assert "Test details" in str(exception)
    assert exception.tool_name == "test_tool"
    assert exception.details == "Test details"
    assert exception.error_code == "TOOL_EXECUTION_ERROR"


def test_tool_execution_exception_no_details():
    """Test ToolExecutionException without details."""
    exception = ToolExecutionException("test_tool")

    assert "test_tool" in str(exception)
    assert exception.tool_name == "test_tool"
    assert exception.details == ""
    assert exception.error_code == "TOOL_EXECUTION_ERROR"


def test_agent_processing_exception():
    """Test AgentProcessingException."""
    exception = AgentProcessingException("Processing failed")

    assert "Processing failed" in str(exception)
    assert exception.details == "Processing failed"
    assert exception.error_code == "AGENT_PROCESSING_ERROR"


def test_agent_processing_exception_no_details():
    """Test AgentProcessingException without details."""
    exception = AgentProcessingException()

    assert "processing request with AI agent" in str(exception).lower()
    assert exception.details == ""
    assert exception.error_code == "AGENT_PROCESSING_ERROR"


def test_invalid_request_exception():
    """Test InvalidRequestException."""
    exception = InvalidRequestException("title", "Too long")

    assert "title" in str(exception)
    assert "Too long" in str(exception)
    assert exception.field == "title"
    assert exception.reason == "Too long"
    assert exception.error_code == "INVALID_REQUEST"


def test_rate_limit_exceeded_exception():
    """Test RateLimitExceededException."""
    exception = RateLimitExceededException("api_calls")

    assert "api_calls" in str(exception)
    assert exception.limit_type == "api_calls"
    assert exception.error_code == "RATE_LIMIT_EXCEEDED"


def test_rate_limit_exceeded_exception_default():
    """Test RateLimitExceededException with default."""
    exception = RateLimitExceededException()

    assert "request" in str(exception)
    assert exception.limit_type == "request"
    assert exception.error_code == "RATE_LIMIT_EXCEEDED"


def test_database_connection_exception():
    """Test DatabaseConnectionException."""
    exception = DatabaseConnectionException("Connection failed")

    assert "Connection failed" in str(exception)
    assert exception.details == "Connection failed"
    assert exception.error_code == "DATABASE_CONNECTION_ERROR"


def test_database_connection_exception_no_details():
    """Test DatabaseConnectionException without details."""
    exception = DatabaseConnectionException()

    assert "Database connection error" in str(exception)
    assert exception.details == ""
    assert exception.error_code == "DATABASE_CONNECTION_ERROR"