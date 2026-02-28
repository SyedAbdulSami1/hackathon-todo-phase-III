"""Service layer for conversation management."""

from typing import List, Optional
from sqlmodel import Session, select
from models.conversation import Conversation
from models.message import Message
from datetime import datetime


class ConversationService:
    """Service class for managing conversations."""

    def __init__(self, session: Session):
        self.session = session

    def create_conversation(self, user_id: str, title: Optional[str] = None) -> Conversation:
        """Create a new conversation."""
        conversation = Conversation(
            user_id=user_id,
            title=title,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)
        return conversation

    def get_conversation_by_id(self, conversation_id: str) -> Optional[Conversation]:
        """Retrieve a conversation by its ID."""
        return self.session.get(Conversation, conversation_id)

    def get_user_conversations(self, user_id: str) -> List[Conversation]:
        """Retrieve all conversations for a specific user."""
        statement = select(Conversation).where(Conversation.user_id == user_id)
        return self.session.exec(statement).all()

    def update_conversation_title(self, conversation_id: str, title: str) -> Optional[Conversation]:
        """Update the title of a conversation."""
        conversation = self.session.get(Conversation, conversation_id)
        if conversation:
            conversation.title = title
            conversation.updated_at = datetime.utcnow()
            self.session.add(conversation)
            self.session.commit()
            self.session.refresh(conversation)
        return conversation

    def delete_conversation(self, conversation_id: str) -> bool:
        """Delete a conversation and all its messages."""
        conversation = self.session.get(Conversation, conversation_id)
        if conversation:
            # Delete all messages in the conversation first
            statement = select(Message).where(Message.conversation_id == conversation_id)
            messages = self.session.exec(statement).all()
            for message in messages:
                self.session.delete(message)

            # Then delete the conversation
            self.session.delete(conversation)
            self.session.commit()
            return True
        return False

    def update_conversation_timestamp(self, conversation_id: str) -> Optional[Conversation]:
        """Update the updated_at timestamp for a conversation."""
        conversation = self.session.get(Conversation, conversation_id)
        if conversation:
            conversation.updated_at = datetime.utcnow()
            self.session.add(conversation)
            self.session.commit()
            self.session.refresh(conversation)
        return conversation
