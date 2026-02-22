"""Chat endpoint router for the AI Chatbot feature."""

from fastapi import APIRouter, Depends, HTTPException, Header
from typing import Dict, Any
from uuid import uuid4
from sqlmodel import Session
from backend.schemas.chat import ChatRequest, ChatResponse
from backend.db import get_session, engine
from backend.models.conversation import Conversation
from backend.models.message import Message, SenderType
from backend.main import get_chat_agent
from dependencies.auth import get_current_user
from models import User


router = APIRouter()


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Process natural language input and return appropriate response.

    Args:
        user_id: The ID of the user making the request (must match authenticated user)
        request: The chat request containing the message and optional conversation ID
        current_user: The authenticated user (from JWT token)

    Returns:
        ChatResponse containing the AI response and metadata
    """
    try:
        # Verify that the user_id in the path matches the authenticated user
        # This is a simplified check - in a real implementation, you'd compare with user.id
        if str(current_user.id) != user_id:
            raise HTTPException(
                status_code=403,
                detail="Forbidden: You can only access your own chat"
            )

        # Get the global chat agent
        agent = get_chat_agent()
        if not agent:
            raise HTTPException(status_code=500, detail="Chat agent not initialized")

        # Determine conversation ID - create new if not provided
        conversation_id = request.conversation_id
        if not conversation_id:
            # Create a new conversation
            conversation = Conversation(user_id=user_id)
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
            conversation_id = str(conversation.id)
        else:
            # Try to retrieve existing conversation
            conversation = session.get(Conversation, conversation_id)
            if not conversation:
                # If conversation doesn't exist, create a new one
                conversation = Conversation(user_id=user_id)
                session.add(conversation)
                session.commit()
                session.refresh(conversation)
                conversation_id = str(conversation.id)
            elif conversation.user_id != user_id:
                # Verify the conversation belongs to the user
                raise HTTPException(
                    status_code=403,
                    detail="Forbidden: You can only access your own conversations"
                )

        # Process the user's message using the agent
        result = agent.process_request(request.message)

        # Create user message record
        user_message = Message(
            conversation_id=conversation_id,
            sender_type=SenderType.USER,
            content=request.message,
            message_type="text"
        )
        session.add(user_message)

        # Create assistant message record
        assistant_message = Message(
            conversation_id=conversation_id,
            sender_type=SenderType.ASSISTANT,
            content=result["response"],
            message_type="text",
            tool_used=result.get("tool_used"),
            tool_result=result.get("tool_result")
        )
        session.add(assistant_message)
        session.commit()

        # Update conversation's updated_at timestamp
        from datetime import datetime
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)
        session.commit()

        # Construct response
        response = ChatResponse(
            response=result["response"],
            conversation_id=str(conversation_id),
            message_id=str(assistant_message.id),
            tool_used=result.get("tool_used"),
            actions_taken=result.get("actions_taken", [])
        )

        return response

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log the error (in a real implementation)
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{user_id}/conversations")
async def get_user_conversations(
    user_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all conversations for a specific user."""
    try:
        # Verify that the user_id matches the authenticated user
        if str(current_user.id) != user_id:
            raise HTTPException(
                status_code=403,
                detail="Forbidden: You can only access your own conversations"
            )

        conversations = session.query(Conversation).filter(Conversation.user_id == user_id).all()
        return [{"id": str(conv.id), "title": conv.title, "created_at": conv.created_at, "updated_at": conv.updated_at}
                for conv in conversations]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving conversations: {str(e)}")


@router.get("/{user_id}/conversations/{conversation_id}")
async def get_conversation_history(
    user_id: str,
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get the history of a specific conversation."""
    try:
        # Verify that the user_id matches the authenticated user
        if str(current_user.id) != user_id:
            raise HTTPException(
                status_code=403,
                detail="Forbidden: You can only access your own conversations"
            )

        # Verify that the conversation belongs to the user
        conversation = session.get(Conversation, conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise HTTPException(status_code=404, detail="Conversation not found or access denied")

        # Get messages for this conversation
        messages = session.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.timestamp).all()

        return {
            "conversation_id": str(conversation_id),
            "messages": [
                {
                    "id": str(msg.id),
                    "sender_type": msg.sender_type.value,
                    "content": msg.content,
                    "timestamp": msg.timestamp,
                    "tool_used": msg.tool_used,
                    "tool_result": msg.tool_result
                } for msg in messages
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving conversation history: {str(e)}")