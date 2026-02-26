"""Service for loading conversation data and history."""

from typing import Dict, Any, List, Optional
from sqlmodel import Session
from services.conversation_service import ConversationService
from services.message_service import MessageService
from models.conversation import Conversation
from models.message import Message


class ConversationLoader:
    """Service for loading conversation and message history."""

    def __init__(self, session: Session):
        self.session = session
        self.conversation_service = ConversationService(session)
        self.message_service = MessageService(session)

    def load_conversation_history(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """Load the history for a specific conversation."""
        conversation = self.conversation_service.get_conversation_by_id(conversation_id)
        if not conversation:
            return None

        messages = self.message_service.get_messages_for_conversation(conversation_id)

        return {
            "conversation_id": str(conversation.id),
            "user_id": str(conversation.user_id),
            "title": conversation.title,
            "messages": [
                {
                    "id": str(msg.id),
                    "role": msg.sender_type.value,
                    "content": msg.content,
                    "timestamp": msg.created_at.isoformat() if msg.created_at else None,
                    "message_type": msg.message_type,
                    "tool_used": msg.tool_used,
                    "tool_result": msg.tool_result
                }
                for msg in messages
            ],
            "metadata": conversation.metadata_json,
            "created_at": conversation.created_at.isoformat() if conversation.created_at else None,
            "updated_at": conversation.updated_at.isoformat() if conversation.updated_at else None
        }

    def get_user_conversations_list(self, user_id: str) -> List[Dict[str, Any]]:
        """Get a list of all conversations for a user."""
        conversations = self.conversation_service.get_user_conversations(user_id)

        return [
            {
                "id": str(conv.id),
                "title": conv.title,
                "updated_at": conv.updated_at.isoformat() if conv.updated_at else None,
                "message_count": len(self.message_service.get_messages_for_conversation(str(conv.id)))
            }
            for conv in conversations
        ]

    def get_latest_conversation(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get the most recent conversation for a user."""
        conversations = self.conversation_service.get_user_conversations(user_id)
        if not conversations:
            return None

        # Conversations are usually sorted by updated_at descending
        latest = conversations[0]
        return self.load_conversation_history(str(latest.id))
