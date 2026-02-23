"""Message model for the AI Chatbot feature."""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlalchemy import DateTime, String
from sqlmodel import Field, Relationship, SQLModel


class SenderType(str, Enum):
    """Enumeration for message sender types."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class MessageType(str, Enum):
    """Enumeration for message types."""
    TEXT = "text"
    TOOL_CALL = "tool_call"
    TOOL_RESPONSE = "tool_response"


class Message(SQLModel, table=True):
    """Represents individual exchanges within a conversation."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversation.id", index=True)
    sender_type: SenderType = Field(index=True)
    content: str = Field(nullable=False)  # The actual message content
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False)
    )
    tool_used: Optional[str] = None  # Name of MCP tool used in response
    tool_parameters: Optional[dict] = Field(default=None, sa_column=sa.Column(sa.JSON))  # Parameters passed to the MCP tool
    tool_result: Optional[dict] = Field(default=None, sa_column=sa.Column(sa.JSON))  # Result returned by the MCP tool
    message_type: Optional[MessageType] = Field(default=None)  # Type of the message

    # Relationship to conversation
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")

    class Config:
        arbitrary_types_allowed = True
