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

def get_chat_agent():
    """Get the global chat agent instance."""
    # Import inside function to avoid circular dependency
    from index import get_chat_agent as get_global_agent
    return get_global_agent()

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
    print(f"DEBUG: Chat endpoint reached for user {user_id}")
    try:
        # Verify that the user_id in the path matches the authenticated user
        if str(current_user.id) != str(user_id):
            print(f"DEBUG: User ID mismatch: {current_user.id} vs {user_id}")
            raise HTTPException(
                status_code=403,
                detail="Forbidden: You can only access your own chat"
            )

        # Get the global chat agent
        print(f"DEBUG: Getting chat agent...")
        agent = get_chat_agent()
        if not agent:
            print(f"DEBUG: Chat agent is None!")
            raise HTTPException(status_code=500, detail="Chat agent not initialized")

        # Determine conversation ID - create new if not provided
        conversation_id = request.conversation_id
        print(f"DEBUG: Conversation ID from request: {conversation_id}")
        
        if not conversation_id:
            print(f"DEBUG: Creating new conversation...")
            conversation = Conversation(user_id=user_id)
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
            conversation_id = str(conversation.id)
            print(f"DEBUG: New conversation created: {conversation_id}")
        else:
            print(f"DEBUG: Looking up existing conversation...")
            from uuid import UUID
            try:
                conv_uuid = UUID(conversation_id)
                conversation = session.get(Conversation, conv_uuid)
            except ValueError:
                print(f"DEBUG: Invalid UUID format: {conversation_id}")
                conversation = None
                
            if not conversation:
                print(f"DEBUG: Conversation not found, creating new...")
                conversation = Conversation(user_id=user_id)
                session.add(conversation)
                session.commit()
                session.refresh(conversation)
                conversation_id = str(conversation.id)
            elif str(conversation.user_id) != str(user_id):
                print(f"DEBUG: Conversation ownership mismatch: {conversation.user_id} vs {user_id}")
                raise HTTPException(
                    status_code=403,
                    detail="Forbidden: You can only access your own conversations"
                )

        # 1. Fetch conversation history from database
        print(f"DEBUG: Fetching history for {conversation_id}...")
        history_messages = []
        db_history = session.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.timestamp).all()
        for msg in db_history:
            history_messages.append({
                "role": msg.sender_type.value,
                "content": msg.content
            })
        print(f"DEBUG: Found {len(history_messages)} history messages")

        # 3. Store user message in database
        print(f"DEBUG: Storing user message...")
        from uuid import UUID
        user_message = Message(
            conversation_id=UUID(conversation_id) if isinstance(conversation_id, str) else conversation_id,
            sender_type=SenderType.USER,
            content=request.message,
            message_type="text"
        )
        session.add(user_message)
        session.commit()

        # 4. Run agent with history context
        print(f"DEBUG: Calling agent.process_request...")
        result = await agent.process_request(request.message, user_id=str(current_user.id), conversation_context=history_messages)
        print(f"DEBUG: Agent responded: {result.get('response')[:50]}...")

        # 5. Store assistant response in database
        print(f"DEBUG: Storing assistant response...")
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
        print(f"DEBUG: Chat endpoint completed successfully")

        # 6. Return response
        return ChatResponse(
            conversation_id=str(conversation_id),
            response=result["response"],
            tool_calls=result.get("tool_calls", []),
            message_id=str(assistant_message.id),
            actions_taken=result.get("actions_taken", [])
        )

    except HTTPException as e:
        print(f"DEBUG: HTTP Error in chat endpoint: {e.detail}")
        raise
    except Exception as e:
        print(f"DEBUG: UNEXPECTED ERROR in chat endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


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
