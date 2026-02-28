"""Logger for chatbot interactions and error tracking."""

import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional


class ChatLogger:
    """Logger for chatbot interactions and error tracking."""

    def __init__(self, name: str = "chatbot"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # Prevent adding multiple handlers if logger already has them
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def log_interaction(self, user_id: str, conversation_id: str,
                       user_input: str, ai_response: str,
                       tools_used: Optional[list] = None):
        """Log a chat interaction."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "chat_interaction",
            "user_id": user_id,
            "conversation_id": conversation_id,
            "user_input": user_input,
            "ai_response": ai_response,
            "tools_used": tools_used or [],
            "interaction_id": self._generate_interaction_id()
        }

        self.logger.info(json.dumps(log_data))

    def log_tool_execution(self, tool_name: str, parameters: Dict[str, Any],
                          result: Dict[str, Any], execution_time: float,
                          user_id: str = None, conversation_id: str = None):
        """Log an MCP tool execution."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "tool_execution",
            "tool_name": tool_name,
            "parameters": parameters,
            "result": result,
            "execution_time_ms": execution_time,
            "user_id": user_id,
            "conversation_id": conversation_id,
            "success": result.get("success", False)
        }

        if result.get("success", True):
            self.logger.info(json.dumps(log_data))
        else:
            self.logger.warning(json.dumps(log_data))

    def log_error(self, error_type: str, error_message: str,
                 user_id: str = None, conversation_id: str = None,
                 additional_info: Optional[Dict[str, Any]] = None):
        """Log an error."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "error",
            "error_type": error_type,
            "error_message": error_message,
            "user_id": user_id,
            "conversation_id": conversation_id,
            "additional_info": additional_info or {}
        }

        self.logger.error(json.dumps(log_data))

    def log_agent_processing(self, user_input: str, parsed_intent: Dict[str, Any],
                           processing_time: float, user_id: str = None,
                           conversation_id: str = None):
        """Log AI agent processing."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "agent_processing",
            "user_input": user_input,
            "parsed_intent": parsed_intent,
            "processing_time_ms": processing_time,
            "user_id": user_id,
            "conversation_id": conversation_id
        }

        self.logger.info(json.dumps(log_data))

    def log_conversation_start(self, conversation_id: str, user_id: str,
                             initial_message: str = None):
        """Log the start of a new conversation."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "conversation_start",
            "conversation_id": conversation_id,
            "user_id": user_id,
            "initial_message": initial_message
        }

        self.logger.info(json.dumps(log_data))

    def log_conversation_end(self, conversation_id: str, user_id: str,
                           message_count: int, duration: float):
        """Log the end of a conversation."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "conversation_end",
            "conversation_id": conversation_id,
            "user_id": user_id,
            "message_count": message_count,
            "duration_seconds": duration
        }

        self.logger.info(json.dumps(log_data))

    def _generate_interaction_id(self) -> str:
        """Generate a unique interaction ID."""
        import uuid
        return str(uuid.uuid4())

    def set_level(self, level: int):
        """Set the logging level."""
        self.logger.setLevel(level)


# Global logger instance
chat_logger = ChatLogger()
