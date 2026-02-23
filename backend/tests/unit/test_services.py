"""Unit tests for the AI Chatbot services."""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from uuid import uuid4

from services.conversation_service import ConversationService
from services.message_service import MessageService
from services.conversation_loader import ConversationLoader
from services.conversation_persistence import ConversationPersistence
from models.conversation import Conversation
from models.message import Message, SenderType


def test_conversation_service_create_conversation():
    """Test ConversationService create_conversation method."""
    mock_session = Mock()
    conversation_service = ConversationService(mock_session)

    conversation = conversation_service.create_conversation("test_user", "Test Title")

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()


def test_conversation_service_get_conversation_by_id():
    """Test ConversationService get_conversation_by_id method."""
    mock_session = Mock()
    conversation_service = ConversationService(mock_session)

    conversation_id = "test_id"
    conversation_service.get_conversation_by_id(conversation_id)

    mock_session.get.assert_called_once_with(Conversation, conversation_id)


def test_conversation_service_get_user_conversations():
    """Test ConversationService get_user_conversations method."""
    mock_session = Mock()
    mock_statement = Mock()
    mock_exec = Mock()
    mock_exec.all.return_value = []
    mock_session.exec.return_value = mock_exec

    conversation_service = ConversationService(mock_session)

    conversations = conversation_service.get_user_conversations("test_user")

    # Verify that the select statement was called properly
    mock_session.exec.assert_called_once()


def test_conversation_service_update_conversation_title():
    """Test ConversationService update_conversation_title method."""
    mock_session = Mock()
    mock_conversation = Mock()
    mock_conversation.id = "test_id"
    mock_session.get.return_value = mock_conversation

    conversation_service = ConversationService(mock_session)

    result = conversation_service.update_conversation_title("test_id", "New Title")

    assert result == mock_conversation
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


def test_conversation_service_delete_conversation():
    """Test ConversationService delete_conversation method."""
    mock_session = Mock()
    mock_conversation = Mock()
    mock_session.get.return_value = mock_conversation

    conversation_service = ConversationService(mock_session)

    result = conversation_service.delete_conversation("test_id")

    assert result is True
    mock_session.delete.assert_called_once_with(mock_conversation)
    mock_session.commit.assert_called_once()


def test_message_service_create_message():
    """Test MessageService create_message method."""
    mock_session = Mock()
    message_service = MessageService(mock_session)

    conversation_id = str(uuid4())
    message = message_service.create_message(
        conversation_id,
        SenderType.USER,
        "Test content"
    )

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()


def test_message_service_get_message_by_id():
    """Test MessageService get_message_by_id method."""
    mock_session = Mock()
    message_service = MessageService(mock_session)

    message_id = str(uuid4())
    message_service.get_message_by_id(message_id)

    mock_session.get.assert_called_once_with(Message, message_id)


def test_message_service_get_messages_for_conversation():
    """Test MessageService get_messages_for_conversation method."""
    mock_session = Mock()
    mock_statement = Mock()
    mock_exec = Mock()
    mock_exec.all.return_value = []
    mock_session.exec.return_value = mock_exec

    message_service = MessageService(mock_session)

    messages = message_service.get_messages_for_conversation("test_conv_id")

    # Verify that the select statement was called properly
    mock_session.exec.assert_called_once()


def test_message_service_update_message_content():
    """Test MessageService update_message_content method."""
    mock_session = Mock()
    mock_message = Mock()
    mock_session.get.return_value = mock_message

    message_service = MessageService(mock_session)

    result = message_service.update_message_content("test_msg_id", "New content")

    assert result == mock_message
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


def test_message_service_delete_message():
    """Test MessageService delete_message method."""
    mock_session = Mock()
    mock_message = Mock()
    mock_session.get.return_value = mock_message

    message_service = MessageService(mock_session)

    result = message_service.delete_message("test_msg_id")

    assert result is True
    mock_session.delete.assert_called_once_with(mock_message)
    mock_session.commit.assert_called_once()


def test_conversation_loader_initialization():
    """Test ConversationLoader initialization."""
    mock_session = Mock()
    conversation_loader = ConversationLoader(mock_session)

    assert conversation_loader.session == mock_session
    assert conversation_loader.conversation_service is not None
    assert conversation_loader.message_service is not None


def test_conversation_persistence_initialization():
    """Test ConversationPersistence initialization."""
    mock_session = Mock()
    conversation_persistence = ConversationPersistence(mock_session)

    assert conversation_persistence.session == mock_session
    assert conversation_persistence.conversation_service is not None
    assert conversation_persistence.message_service is not None


def test_conversation_persistence_save_new_conversation():
    """Test ConversationPersistence save_new_conversation method."""
    mock_session = Mock()
    mock_conversation = Mock()
    mock_conversation.id = "test_conv_id"
    mock_conversation_service = Mock()
    mock_conversation_service.create_conversation.return_value = mock_conversation

    with patch('services.conversation_persistence.ConversationService', return_value=mock_conversation_service):
        conversation_persistence = ConversationPersistence(mock_session)

        result = conversation_persistence.save_new_conversation("test_user", "Initial message", "Test Title")

        assert result["conversation_id"] == "test_conv_id"
        assert result["created"] is True


def test_conversation_persistence_save_message():
    """Test ConversationPersistence save_message method."""
    mock_session = Mock()
    mock_message = Mock()
    mock_message.id = "test_msg_id"
    mock_message_service = Mock()
    mock_message_service.create_message.return_value = mock_message

    with patch('services.conversation_persistence.MessageService', return_value=mock_message_service):
        conversation_persistence = ConversationPersistence(mock_session)

        result = conversation_persistence.save_message(
            "test_conv_id",
            SenderType.USER,
            "Test content"
        )

        assert result["message_id"] == "test_msg_id"
        assert result["saved"] is True


def test_conversation_persistence_save_assistant_response():
    """Test ConversationPersistence save_assistant_response method."""
    mock_session = Mock()
    mock_message = Mock()
    mock_message.id = "test_msg_id"
    mock_message_service = Mock()
    mock_message_service.create_message.return_value = mock_message

    with patch('services.conversation_persistence.MessageService', return_value=mock_message_service):
        conversation_persistence = ConversationPersistence(mock_session)

        result = conversation_persistence.save_assistant_response(
            "test_conv_id",
            "Assistant response"
        )

        assert "message_id" in result
        assert result["saved"] is True


def test_conversation_loader_load_conversation_history():
    """Test ConversationLoader load_conversation_history method."""
    mock_session = Mock()
    mock_conversation_service = Mock()
    mock_message_service = Mock()

    # Mock a conversation
    mock_conversation = Mock()
    mock_conversation.id = "test_conv_id"
    mock_conversation.user_id = "test_user"
    mock_conversation.title = "Test Title"
    mock_conversation.created_at = datetime.utcnow()
    mock_conversation.updated_at = datetime.utcnow()

    mock_conversation_service.get_conversation_by_id.return_value = mock_conversation
    mock_message_service.get_messages_for_conversation.return_value = []

    with patch('services.conversation_loader.ConversationService', return_value=mock_conversation_service), \
         patch('services.conversation_loader.MessageService', return_value=mock_message_service):

        conversation_loader = ConversationLoader(mock_session)

        history = conversation_loader.load_conversation_history("test_conv_id")

        assert history is not None
        assert history["conversation_id"] == "test_conv_id"
        assert history["user_id"] == "test_user"


def test_conversation_loader_load_conversation_history_none():
    """Test ConversationLoader load_conversation_history with non-existent conversation."""
    mock_session = Mock()
    mock_conversation_service = Mock()
    mock_conversation_service.get_conversation_by_id.return_value = None

    with patch('services.conversation_loader.ConversationService', return_value=mock_conversation_service), \
         patch('services.conversation_loader.MessageService'):

        conversation_loader = ConversationLoader(mock_session)

        history = conversation_loader.load_conversation_history("nonexistent_id")

        assert history is None