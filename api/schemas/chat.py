"""Schema definitions for chat endpoints."""

from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str
    conversation_id: Optional[str] = None  # Optional existing conversation ID


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    conversation_id: str
    response: str
    tool_calls: List[dict] = []  # Requirement #7: tool_calls (array)
    message_id: str
    actions_taken: List[str] = []


class ChatHistoryResponse(BaseModel):
    """Response model for chat history."""
    conversation_id: str
    messages: List[dict]  # List of message objects
