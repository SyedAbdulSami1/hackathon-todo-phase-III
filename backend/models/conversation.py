"""Conversation model for the AI Chatbot feature."""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String, func
from sqlmodel import Field, SQLModel


class Conversation(SQLModel, table=True):
    """Represents a single chat session between a user and the AI assistant."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(sa_column=String, index=True, nullable=False)  # Foreign key to user
    title: Optional[str] = Field(sa_column=String(200))  # Optional conversation title
    created_at: datetime = Field(
        sa_column=DateTime(timezone=True), default_factory=datetime.utcnow
    )
    updated_at: datetime = Field(
        sa_column=DateTime(timezone=True),
        default_factory=datetime.utcnow,
        nullable=False
    )
    metadata_json: Optional[dict] = Field(default=None)  # Additional context data

    class Config:
        arbitrary_types_allowed = True