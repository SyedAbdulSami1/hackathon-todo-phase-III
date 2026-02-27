"""Unit tests for the AI Chatbot services."""

import pytest
from unittest.mock import Mock, patch, MagicMock
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

    conversation_id = str(uuid4())
    conversation_service.get_conversation_by_id(conversation_id)

    mock_session.get.assert_called_once_with(Conversation, conversation_id)


def test_conversation_service_get_user_conversations():
    """Test ConversationService get_user_conversations method."""
    mock_session = Mock()
    mock_exec = Mock()
    mock_exec.all.return_value = []
    mock_session.exec.return_value = mock_exec

    conversation_service = ConversationService(mock_session)

    conversations = conversation_service.get_user_conversations("test_user")

    mock_session.exec.assert_called_once()
    assert conversations == []


def test_conversation_service_update_conversation_title():
    """Test ConversationService update_conversation_title method."""
    mock_session = Mock()
    mock_conversation = Mock()
    mock_session.get.return_value = mock_conversation

    conversation_service = ConversationService(mock_session)

    result = conversation_service.update_conversation_title(str(uuid4()), "New Title")

    assert result == mock_conversation
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


def test_conversation_service_delete_conversation():
    """Test ConversationService delete_conversation method."""
    mock_session = Mock()
    mock_conversation = Mock()
    mock_session.get.return_value = mock_conversation
    
    # Mock the exec().all() for messages
    mock_exec = Mock()
    mock_exec.all.return_value = []
    mock_session.exec.return_value = mock_exec

    conversation_service = ConversationService(mock_session)

    result = conversation_service.delete_conversation(str(uuid4()))

    assert result is True
    mock_session.delete.assert_called()
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
    mock_exec = Mock()
    mock_exec.all.return_value = []
    mock_session.exec.return_value = mock_exec

    message_service = MessageService(mock_session)

    messages = message_service.get_messages_for_conversation(str(uuid4()))

    mock_session.exec.assert_called_once()
    assert messages == []


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
    mock_conversation.id = uuid4()
    
    # We need to mock the conversation_service within persistence
    with patch('services.conversation_persistence.ConversationService') as mock_service_class:
        mock_service = mock_service_class.return_value
        mock_service.create_conversation.return_value = mock_conversation
        
        conversation_persistence = ConversationPersistence(mock_session)
        result = conversation_persistence.save_new_conversation("test_user", "Initial message", "Test Title")

        assert result["conversation_id"] == str(mock_conversation.id)
        assert result["created"] is True


def test_conversation_persistence_save_message():
    """Test ConversationPersistence save_message method."""
    mock_session = Mock()
    mock_message = Mock()
    mock_message.id = uuid4()
    
    with patch('services.conversation_persistence.MessageService') as mock_service_class:
        mock_service = mock_service_class.return_value
        mock_service.create_message.return_value = mock_message
        
        conversation_persistence = ConversationPersistence(mock_session)
        result = conversation_persistence.save_message(
            str(uuid4()),
            SenderType.USER,
            "Test content"
        )

        assert result["message_id"] == str(mock_message.id)
        assert result["saved"] is True


def test_conversation_loader_load_conversation_history():
    """Test ConversationLoader load_conversation_history method."""
    mock_session = Mock()
    
    # Mock a conversation
    mock_conversation = Mock()
    mock_conversation.id = uuid4()
    mock_conversation.user_id = "test_user"
    mock_conversation.title = "Test Title"
    mock_conversation.metadata_json = None
    mock_conversation.created_at = datetime.utcnow()
    mock_conversation.updated_at = datetime.utcnow()

    with patch('services.conversation_loader.ConversationService') as mock_conv_service_class, \
         patch('services.conversation_loader.MessageService') as mock_msg_service_class:
        
        mock_conv_service = mock_conv_service_class.return_value
        mock_conv_service.get_conversation_by_id.return_value = mock_conversation
        
        mock_msg_service = mock_msg_service_class.return_value
        mock_msg_service.get_messages_for_conversation.return_value = []

        conversation_loader = ConversationLoader(mock_session)
        history = conversation_loader.load_conversation_history(str(mock_conversation.id))

        assert history is not None
        assert history["conversation_id"] == str(mock_conversation.id)
        assert history["user_id"] == "test_user"
