"""AI Chat Agent using OpenAI Tool Calling for MCP todo management."""

import os
import json
from typing import Dict, Any, List, Optional
from openai import OpenAI
from agents.config import AgentConfig
from tools.registry import tool_registry

class ChatAgent:
    """AI agent for processing chat requests using Google Gemini (via OpenAI SDK)."""

    def __init__(self, config: Optional[AgentConfig] = None):
        self.config = config or AgentConfig()
        
        # Using Google's OpenAI-compatible base URL
        api_key = os.getenv("GOOGLE_API_KEY")
        base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
        
        self.model_name = os.getenv("AGENT_MODEL_NAME", "gemini-1.5-flash") # Free model
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.tools = tool_registry

    def process_request(self, user_input: str, conversation_context: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        8-Step Stateless Flow (Requirement #10):
        1. Receive user message
        2. Fetch history (done in router)
        3. Build message array
        4. Run agent with tool-calling
        5. Return response with tool_calls
        """
        # Build the message array for OpenAI
        messages = []
        # Add system prompt for behavior (Requirement #9)
        messages.append({
            "role": "system", 
            "content": "You are a friendly AI Todo Assistant. Use the provided tools to manage the user's tasks. Always confirm actions with a friendly response."
        })
        
        # Add conversation history
        if conversation_context:
            for msg in conversation_context:
                # Map our Message sender types to OpenAI roles
                role = "assistant" if msg["role"] == "assistant" else "user"
                messages.append({"role": role, "content": msg["content"]})
        
        # Add new user message
        messages.append({"role": "user", "content": user_input})

        # Define tools for OpenAI (Requirement #8)
        tools = self._get_tool_definitions()

        try:
            # 1. First call to OpenAI to get tool calls
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )

            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            # 2. If the AI wants to call tools (Requirement #10 Step 6)
            if tool_calls:
                messages.append(response_message)
                actions_taken = []
                tool_results = []

                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    # Execute the MCP tool (Requirement #8)
                    result = self.tools.execute_tool(function_name, **function_args)
                    
                    actions_taken.append(f"Action: {function_name}")
                    tool_results.append({
                        "name": function_name,
                        "args": function_args,
                        "result": result
                    })

                    # Add tool result to history for second completion
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": json.dumps(result)
                    })

                # 3. Second call to get final friendly response (Requirement #9)
                second_response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages
                )
                
                return {
                    "response": second_response.choices[0].message.content,
                    "tool_calls": tool_results,
                    "actions_taken": actions_taken
                }

            # If no tool was called
            return {
                "response": response_message.content,
                "tool_calls": [],
                "actions_taken": ["General interaction"]
            }

        except Exception as e:
            return {
                "response": f"Sorry, I encountered an error: {str(e)}",
                "tool_calls": [],
                "actions_taken": ["Error handling"]
            }

    def _get_tool_definitions(self):
        """Standard tool definitions for OpenAI (Requirement #8)."""
        return [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Create a new task (Requirement #8.1)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "description": {"type": "string"}
                        },
                        "required": ["title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "Retrieve tasks from the list (Requirement #8.2)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "status": {"type": "string", "enum": ["all", "pending", "completed"]}
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as complete (Requirement #8.3)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "integer"}
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Remove a task from the list (Requirement #8.4)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "integer"}
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Modify task title or description (Requirement #8.5)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "integer"},
                            "title": {"type": "string"},
                            "description": {"type": "string"}
                        },
                        "required": ["task_id"]
                    }
                }
            }
        ]
