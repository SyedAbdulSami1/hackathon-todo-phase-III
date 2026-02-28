"""AI Chat Agent using OpenAI Tool Calling for MCP todo management."""

import os
import json
from typing import Dict, Any, List, Optional
from openai import AsyncOpenAI
from agents.config import AgentConfig
from tools.registry import tool_registry

class ChatAgent:
    """AI agent for processing chat requests using Google Gemini (via OpenAI SDK)."""

    def __init__(self, config: Optional[AgentConfig] = None):
        self.config = config or AgentConfig()
        
        # Google's OpenAI-compatible Base URL MUST have the trailing slash
        self.api_key = os.getenv("GOOGLE_API_KEY")
        base_url = os.getenv("AGENT_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
        
        self.model_name = os.getenv("AGENT_MODEL_NAME", "gemini-flash-latest")
        # Override broken model name from .env if present
        if self.model_name == "gemini-1.5-flash":
            print(f"DEBUG: Overriding gemini-1.5-flash with gemini-flash-latest for compatibility")
            self.model_name = "gemini-flash-latest"
            
        print(f"--- ChatAgent Startup ---")
        print(f"Model: {self.model_name}")
        print(f"Base URL: {base_url}")
        
        if not self.api_key:
            print("WARNING: GOOGLE_API_KEY is missing! Agent will fail on requests.")
            
        self.client = AsyncOpenAI(api_key=self.api_key or "missing", base_url=base_url)
        self.tools = tool_registry

    async def process_request(self, user_input: str, user_id: str = "1", conversation_context: Optional[List[Dict]] = None) -> Dict[str, Any]:
        print(f"Processing request for user {user_id}: {user_input}")
        
        if not self.api_key or self.api_key == "missing":
            return {
                "response": "I'm sorry, but my API key is missing or invalid. Please check the backend configuration.",
                "tool_calls": [],
                "actions_taken": ["Auth check"]
            }

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
        tools = self.tools.get_tool_definitions()

        try:
            # 1. First call to OpenAI to get tool calls
            response = await self.client.chat.completions.create(
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
                    
                    # Ensure user_id is passed to tools if they expect it (Requirement #8)
                    # We inject the current user's ID into the tool call
                    function_args["user_id"] = str(user_id)
                    
                    # Execute the MCP tool (Requirement #8)
                    result = await self.tools.execute_tool(function_name, **function_args)
                    
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
                second_response = await self.client.chat.completions.create(
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
            import traceback
            traceback.print_exc()
            return {
                "response": f"Sorry, I encountered an error: {str(e)}",
                "tool_calls": [],
                "actions_taken": ["Error handling"]
            }
