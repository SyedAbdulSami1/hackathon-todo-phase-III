"""Schema definitions for conversation history."""

from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class MessageHistoryItem(BaseModel):
    """Schema for a single message in conversation history."""
    id: str
    conversation_id: str
    sender_type: str
    content: str
    timestamp: str
    message_type: Optional[str] = None
    tool_used: Optional[str] = None
    tool_parameters: Optional[dict] = None
    tool_result: Optional[dict] = None


class ConversationHistoryResponse(BaseModel):
    """Schema for conversation history response."""
    conversation_id: str
    user_id: str
    title: Optional[str] = None
    created_at: str
    updated_at: str
    messages: List[MessageHistoryItem]


class RecentConversationsResponse(BaseModel):
    """Schema for recent conversations response."""
    conversations: List[dict]  # List of conversation summaries


class ConversationContextResponse(BaseModel):
    """Schema for conversation context response."""
    conversation_exists: bool
    context: List[dict]  # List of message dicts
    summary: str
    conversation_metadata: Optional[dict] = None
