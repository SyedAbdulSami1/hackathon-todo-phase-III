"""Unit tests for the AI Chatbot models."""

import pytest
from datetime import datetime
from uuid import UUID
from models.conversation import Conversation
from models.message import Message, SenderType


def test_conversation_creation():
    """Test creating a Conversation model instance."""
    conversation = Conversation(
        user_id="test_user",
        title="Test Conversation"
    )

    assert conversation.user_id == "test_user"
    assert conversation.title == "Test Conversation"
    assert isinstance(conversation.id, UUID)
    assert isinstance(conversation.created_at, datetime)
    assert isinstance(conversation.updated_at, datetime)


def test_conversation_defaults():
    """Test Conversation model default values."""
    conversation = Conversation(user_id="test_user")

    assert conversation.user_id == "test_user"
    assert conversation.title is None
    assert isinstance(conversation.id, UUID)


def test_message_creation():
    """Test creating a Message model instance."""
    from uuid import uuid4

    conversation_id = uuid4()
    message = Message(
        conversation_id=conversation_id,
        sender_type=SenderType.USER,
        content="Test message content"
    )

    assert message.conversation_id == conversation_id
    assert message.sender_type == SenderType.USER
    assert message.content == "Test message content"
    assert isinstance(message.id, UUID)
    assert isinstance(message.timestamp, datetime)


def test_message_enum_values():
    """Test that sender_type enum values are correctly enforced."""
    from uuid import uuid4

    conversation_id = uuid4()

    # Test all valid enum values
    message_user = Message(
        conversation_id=conversation_id,
        sender_type=SenderType.USER,
        content="Test message"
    )
    assert message_user.sender_type == SenderType.USER

    message_assistant = Message(
        conversation_id=conversation_id,
        sender_type=SenderType.ASSISTANT,
        content="Test message"
    )
    assert message_assistant.sender_type == SenderType.ASSISTANT

    message_system = Message(
        conversation_id=conversation_id,
        sender_type=SenderType.SYSTEM,
        content="Test message"
    )
    assert message_system.sender_type == SenderType.SYSTEM


def test_message_optional_fields():
    """Test optional fields in Message model."""
    from uuid import uuid4

    conversation_id = uuid4()
    message = Message(
        conversation_id=conversation_id,
        sender_type=SenderType.USER,
        content="Test message content",
        tool_used="test_tool",
        tool_parameters={"param": "value"},
        tool_result={"result": "success"}
    )

    assert message.tool_used == "test_tool"
    assert message.tool_parameters == {"param": "value"}
    assert message.tool_result == {"result": "success"}
