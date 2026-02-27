"""Service layer for message management."""

from typing import List, Optional
from sqlmodel import Session, select
from models.message import Message, SenderType
from datetime import datetime


class MessageService:
    """Service class for managing messages."""

    def __init__(self, session: Session):
        self.session = session

    def create_message(
        self,
        conversation_id: str,
        sender_type: SenderType,
        content: str,
        message_type: Optional[str] = None,
        tool_used: Optional[str] = None,
        tool_parameters: Optional[dict] = None,
        tool_result: Optional[dict] = None
    ) -> Message:
        """Create a new message."""
        message = Message(
            conversation_id=conversation_id,
            sender_type=sender_type,
            content=content,
            message_type=message_type,
            tool_used=tool_used,
            tool_parameters=tool_parameters,
            tool_result=tool_result,
            timestamp=datetime.utcnow()
        )
        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)
        return message

    def get_message_by_id(self, message_id: str) -> Optional[Message]:
        """Retrieve a message by its ID."""
        return self.session.get(Message, message_id)

    def get_messages_for_conversation(self, conversation_id: str) -> List[Message]:
        """Retrieve all messages for a specific conversation."""
        statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.timestamp)
        return self.session.exec(statement).all()

    def get_messages_by_sender(self, conversation_id: str, sender_type: SenderType) -> List[Message]:
        """Retrieve all messages from a specific sender in a conversation."""
        statement = select(Message).where(
            Message.conversation_id == conversation_id,
            Message.sender_type == sender_type
        ).order_by(Message.timestamp)
        return self.session.exec(statement).all()

    def update_message_content(self, message_id: str, content: str) -> Optional[Message]:
        """Update the content of a message."""
        message = self.session.get(Message, message_id)
        if message:
            message.content = content
            self.session.add(message)
            self.session.commit()
            self.session.refresh(message)
        return message

    def delete_message(self, message_id: str) -> bool:
        """Delete a message."""
        message = self.session.get(Message, message_id)
        if message:
            self.session.delete(message)
            self.session.commit()
            return True
        return False

    def get_recent_messages(self, conversation_id: str, limit: int = 10) -> List[Message]:
        """Retrieve the most recent messages for a conversation."""
        statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.timestamp.desc()).limit(limit)
        messages = self.session.exec(statement).all()
        # Return in chronological order (oldest first)
        return list(reversed(messages))
