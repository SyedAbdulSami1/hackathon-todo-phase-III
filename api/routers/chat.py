"""Chat endpoint router for the AI Chatbot feature."""

from fastapi import APIRouter, Depends, HTTPException, Header
from typing import Dict, Any
from uuid import uuid4
from sqlmodel import Session
from schemas.chat import ChatRequest, ChatResponse
from db import get_session, engine

# Handle model imports with fallback for testing
try:
    from models.conversation import Conversation
    from models.message import Message, SenderType
    from models import User
except ImportError:
    from models.conversation import Conversation
    from models.message import Message, SenderType
    from models import User

from dependencies.auth import get_current_user

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
    """
    try:
        # Import inside function to avoid circular dependency
        from main import get_chat_agent

        # Verify that the user_id in the path matches the authenticated user
        # user_id from path is string, current_user.id is int
        if str(current_user.id) != str(user_id):
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
            from uuid import UUID
            try:
                conv_uuid = UUID(conversation_id)
                conversation = session.get(Conversation, conv_uuid)
            except ValueError:
                # If invalid UUID string, treat as not found
                conversation = None
                
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

        # 1. Fetch conversation history from database (Requirement #10 Step 2)
        history_messages = []
        if request.conversation_id:
            db_history = session.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.timestamp).all()
            for msg in db_history:
                history_messages.append({
                    "role": msg.sender_type.value,
                    "content": msg.content
                })

        # 2. Build array for agent: history + new message (Requirement #10 Step 3)
        # Note: ChatAgent handles adding the new message internally in our refined version

        # 3. Store user message in database (Requirement #10 Step 4)
        from uuid import UUID
        user_message = Message(
            conversation_id=UUID(conversation_id) if isinstance(conversation_id, str) else conversation_id,
            sender_type=SenderType.USER,
            content=request.message,
            message_type="text"
        )
        session.add(user_message)
        session.commit()

        # 4. Run agent with history context (Requirement #10 Step 5)
        # Pass user_id so tools can act on the correct user's tasks
        result = await agent.process_request(request.message, user_id=str(current_user.id), conversation_context=history_messages)

        # 5. Store assistant response in database (Requirement #10 Step 7)
        # Handle multiple tool calls by taking the first one for the single-column storage
        primary_tool = None
        primary_result = None
        if result.get("tool_calls") and len(result["tool_calls"]) > 0:
            primary_tool = result["tool_calls"][0]["name"]
            primary_result = result["tool_calls"][0]["result"]

        assistant_message = Message(
            conversation_id=UUID(conversation_id) if isinstance(conversation_id, str) else conversation_id,
            sender_type=SenderType.ASSISTANT,
            content=result["response"],
            message_type="text",
            tool_used=primary_tool,
            tool_result=primary_result
        )
        session.add(assistant_message)
        session.commit()

        # Update conversation's updated_at timestamp
        from datetime import datetime
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)
        session.commit()

        # 6. Return response with tool_calls (Requirement #10 Step 8)
        # Requirement #7 Response format: conversation_id, response, tool_calls
        return ChatResponse(
            conversation_id=str(conversation_id),
            response=result["response"],
            tool_calls=result.get("tool_calls", []),
            message_id=str(assistant_message.id),
            actions_taken=result.get("actions_taken", [])
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log the error (in a real implementation)
        import traceback
        traceback.print_exc()
        error_msg = f"Internal server error: {str(e)}"
        print(f"Error in chat endpoint: {error_msg}")
        raise HTTPException(status_code=500, detail=error_msg)


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
        from uuid import UUID
        try:
            conv_uuid = UUID(conversation_id)
            conversation = session.get(Conversation, conv_uuid)
        except ValueError:
            raise HTTPException(status_code=404, detail="Invalid conversation ID format")

        if not conversation or conversation.user_id != user_id:
            raise HTTPException(status_code=404, detail="Conversation not found or access denied")

        # Get messages for this conversation
        messages = session.query(Message).filter(Message.conversation_id == conv_uuid).order_by(Message.timestamp).all()

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
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error retrieving conversation history: {str(e)}")
