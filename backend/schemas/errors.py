"""Schema definitions for error responses."""

from typing import Optional, List
from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """Schema for error details."""
    type: str
    code: str
    message: str


class ErrorResponse(BaseModel):
    """Schema for error responses."""
    error: ErrorDetail


class ValidationErrorResponse(BaseModel):
    """Schema for validation error responses."""
    error: ErrorDetail
    field: Optional[str] = None
    value: Optional[str] = None


class ToolErrorResponse(BaseModel):
    """Schema for MCP tool error responses."""
    success: bool
    tool_name: str
    error_type: str
    error_message: str
    fallback_message: str


class ChatErrorResponse(BaseModel):
    """Schema for chat-specific error responses."""
    success: bool
    error_code: str
    error_message: str
    suggestion: Optional[str] = None
    available_alternatives: Optional[List[str]] = None