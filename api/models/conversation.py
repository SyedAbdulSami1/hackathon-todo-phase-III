"""Conversation model for the AI Chatbot feature."""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlalchemy import DateTime, String, func
from sqlmodel import Field, SQLModel, Relationship
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .message import Message


class Conversation(SQLModel, table=True):
    """Represents a single chat session between a user and the AI assistant."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(index=True, nullable=False)  # Foreign key to user
    title: Optional[str] = Field(default=None, max_length=200)  # Optional conversation title
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False)
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False)
    )
    metadata_json: Optional[dict] = Field(default=None, sa_column=sa.Column(sa.JSON))  # Additional context data
    
    messages: List["Message"] = Relationship(back_populates="conversation")

    class Config:
        arbitrary_types_allowed = True
