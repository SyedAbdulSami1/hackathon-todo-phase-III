"""Service for persisting conversation data."""

from typing import Dict, Any, Optional
from sqlmodel import Session
from backend.services.conversation_service import ConversationService
from backend.services.message_service import MessageService
from backend.models.conversation import Conversation
from backend.models.message import Message, SenderType


class ConversationPersistence:
    """Service for persisting conversation and message data."""

    def __init__(self, session: Session):
        self.session = session
        self.conversation_service = ConversationService(session)
        self.message_service = MessageService(session)

    def save_new_conversation(self, user_id: str, initial_message: str = None, title: str = None) -> Dict[str, Any]:
        """Save a new conversation with an optional initial message."""
        # Create the conversation
        conversation = self.conversation_service.create_conversation(user_id, title)

        # If there's an initial message, save it
        if initial_message:
            message = self.message_service.create_message(
                conversation_id=str(conversation.id),
                sender_type=SenderType.USER,
                content=initial_message
            )

        return {
            "conversation_id": str(conversation.id),
            "created": True
        }

    def save_message(self, conversation_id: str, sender_type: SenderType, content: str,
                     message_type: str = None, tool_used: str = None,
                     tool_parameters: dict = None, tool_result: dict = None) -> Dict[str, Any]:
        """Save a new message to a conversation."""
        message = self.message_service.create_message(
            conversation_id=conversation_id,
            sender_type=sender_type,
            content=content,
            message_type=message_type,
            tool_used=tool_used,
            tool_parameters=tool_parameters,
            tool_result=tool_result
        )

        # Update the conversation's last updated timestamp
        self.conversation_service.update_conversation_timestamp(conversation_id)

        return {
            "message_id": str(message.id),
            "saved": True
        }

    def save_assistant_response(self, conversation_id: str, response_content: str,
                               tool_used: str = None, tool_result: dict = None) -> Dict[str, Any]:
        """Save an assistant's response to a conversation."""
        return self.save_message(
            conversation_id=conversation_id,
            sender_type=SenderType.ASSISTANT,
            content=response_content,
            message_type="text",
            tool_used=tool_used,
            tool_result=tool_result
        )

    def save_user_input(self, conversation_id: str, user_input: str) -> Dict[str, Any]:
        """Save a user's input to a conversation."""
        return self.save_message(
            conversation_id=conversation_id,
            sender_type=SenderType.USER,
            content=user_input,
            message_type="text"
        )

    def update_conversation_metadata(self, conversation_id: str, metadata: Dict[str, Any]) -> bool:
        """Update conversation metadata."""
        # In our model, we have a metadata_json field but we'll implement title updates
        # since that's more practical for conversation tracking
        if "title" in metadata:
            conversation = self.conversation_service.update_conversation_title(
                conversation_id, metadata["title"]
            )
            return conversation is not None

        return False

    def save_conversation_summary(self, conversation_id: str, summary: str) -> bool:
        """Save a summary of the conversation as the title."""
        # Use the summary as the conversation title
        conversation = self.conversation_service.update_conversation_title(
            conversation_id, summary[:200]  # Limit title length
        )
        return conversation is not None

    def persist_tool_execution(self, conversation_id: str, tool_name: str,
                              parameters: dict, result: dict) -> Dict[str, Any]:
        """Persist tool execution details in the conversation."""
        # Save the tool call as a message
        tool_call_msg = self.save_message(
            conversation_id=conversation_id,
            sender_type=SenderType.USER,  # From user perspective
            content=f"Tool call: {tool_name}",
            message_type="tool_call",
            tool_used=tool_name,
            tool_parameters=parameters
        )

        # Save the tool result as a message
        tool_result_msg = self.save_message(
            conversation_id=conversation_id,
            sender_type=SenderType.ASSISTANT,  # From assistant perspective
            content=f"Tool result: {result.get('message', str(result))}",
            message_type="tool_response",
            tool_used=tool_name,
            tool_result=result
        )

        return {
            "tool_call_saved": tool_call_msg["saved"],
            "tool_result_saved": tool_result_msg["saved"],
            "tool_call_id": tool_call_msg.get("message_id"),
            "tool_result_id": tool_result_msg.get("message_id")
        }