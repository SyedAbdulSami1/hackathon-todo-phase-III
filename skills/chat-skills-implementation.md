# OpenAI Chat Skills Implementation Guide

## 1. Core Chat Assistant Implementation

### Basic Chat Class
```python
import os
from openai import OpenAI
from typing import List, Dict, Optional, Any
import json
from datetime import datetime

class ChatAssistant:
    """A comprehensive chat assistant with multiple skills"""

    def __init__(self, model: str = "gpt-4-turbo", api_key: Optional[str] = None):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.conversation_history: List[Dict[str, str]] = []
        self.skills = {}
        self.context_window = 4096  # tokens
        self.max_response_tokens = 1000

    def add_skill(self, name: str, skill_func):
        """Add a custom skill to the assistant"""
        self.skills[name] = skill_func

    def get_conversation_summary(self, max_tokens: int = 500) -> str:
        """Summarize conversation to save context"""
        if len(self.conversation_history) <= 2:
            return ""

        summary_prompt = "Summarize this conversation in a concise way, keeping important context:"
        summary_messages = [
            {"role": "system", "content": summary_prompt},
            *self.conversation_history[-10:]  # Last 10 messages
        ]

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=summary_messages,
            max_tokens=max_tokens
        )

        return response.choices[0].message.content

    def process_message(self, user_input: str) -> str:
        """Process user input and generate response"""
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": user_input})

        # Check if any skill should be activated
        skill_response = self._activate_skills(user_input)
        if skill_response:
            return skill_response

        # Generate normal chat response
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                max_tokens=self.max_response_tokens,
                temperature=0.7
            )

            assistant_message = response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": assistant_message})

            # Check conversation length and summarize if needed
            if self._get_total_tokens() > self.context_window * 0.8:
                self._manage_context()

            return assistant_message

        except Exception as e:
            return f"Error: {str(e)}"

    def _activate_skills(self, user_input: str) -> Optional[str]:
        """Check if any skill should be activated"""
        for skill_name, skill_func in self.skills.items():
            if skill_name.lower() in user_input.lower():
                return skill_func(user_input, self)
        return None

    def _get_total_tokens(self) -> int:
        """Estimate total tokens in conversation"""
        # Simple estimation - in production, use tiktoken for accurate counting
        return len(json.dumps(self.conversation_history)) // 4

    def _manage_context(self):
        """Manage context window by summarizing"""
        summary = self.get_conversation_summary()
        if summary:
            # Keep system message, summary, and last few exchanges
            self.conversation_history = [
                self.conversation_history[0],  # System message
                {"role": "system", "content": f"Context summary: {summary}"},
                *self.conversation_history[-4:]  # Last 4 messages
            ]
```

## 2. Skill Implementations

### Weather Skill
```python
def weather_skill(user_input: str, assistant: ChatAssistant) -> str:
    """Get weather information for a location"""
    import requests

    # Extract location from user input
    location = None
    words = user_input.lower().split()
    for i, word in enumerate(words):
        if word in ["in", "at", "for"] and i + 1 < len(words):
            location = " ".join(words[i+1:])
            break

    if not location:
        return "I need to know the location to get weather information. Please specify a city."

    # Use a weather API (example: OpenWeatherMap)
    API_KEY = os.getenv("WEATHER_API_KEY")
    if not API_KEY:
        return "Weather service is not configured."

    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            return f"Could not get weather for {location}."

        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]

        return f"The weather in {location} is {description} with a temperature of {temp}°C."

    except Exception as e:
        return f"Error getting weather: {str(e)}"
```

### Code Assistant Skill
```python
def code_assistant_skill(user_input: str, assistant: ChatAssistant) -> str:
    """Help with coding tasks"""
    if "fix" in user_input.lower() or "debug" in user_input.lower():
        # User wants help fixing code
        return "Please share the code you're having trouble with, and I'll help you fix it."

    elif "explain" in user_input.lower():
        # User wants code explanation
        return "Please share the code you'd like me to explain."

    elif "optimize" in user_input.lower():
        # User wants code optimization
        return "Please share the code you'd like me to optimize."

    else:
        return "I can help with coding tasks! Ask me to fix, explain, or optimize code."
```

### Research Assistant Skill
```python
def research_skill(user_input: str, assistant: ChatAssistant) -> str:
    """Conduct research on a topic"""
    if not any(word in user_input.lower() for word in ["research", "find", "search", "lookup"]):
        return None

    # Extract research topic
    topic = user_input.lower().replace("research", "").replace("find", "").replace("search", "").strip()

    if not topic:
        return "What would you like me to research?"

    # Use web search API or knowledge retrieval
    # This is a placeholder - implement actual search functionality
    return f"I'll help you research {topic}. Let me gather information for you."
```

## 3. Advanced Features

### Function Calling Implementation
```python
class ChatAssistantWithFunctions(ChatAssistant):
    """Chat assistant with function calling capabilities"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.functions = []

    def add_function(self, name: str, description: str, parameters: Dict[str, Any]):
        """Add a function that can be called by the AI"""
        function_def = {
            "name": name,
            "description": description,
            "parameters": parameters
        }
        self.functions.append(function_def)

    def process_message_with_functions(self, user_input: str) -> str:
        """Process message with function calling support"""
        self.conversation_history.append({"role": "user", "content": user_input})

        # If no functions, use regular processing
        if not self.functions:
            return self.process_message(user_input)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                functions=self.functions,
                function_call="auto"
            )

            # Check if function was called
            if response.choices[0].message.function_call:
                function_call = response.choices[0].message.function_call
                function_name = function_call.name
                function_args = json.loads(function_call.arguments)

                # Execute the function
                if function_name in self.skills:
                    result = self.skills[function_name](function_args)

                    # Add function result to conversation
                    self.conversation_history.append({
                        "role": "function",
                        "name": function_name,
                        "content": str(result)
                    })

                    # Generate response based on function result
                    follow_up = self.client.chat.completions.create(
                        model=self.model,
                        messages=self.conversation_history
                    )

                    assistant_message = follow_up.choices[0].message.content
                    self.conversation_history.append({"role": "assistant", "content": assistant_message})

                    return assistant_message
                else:
                    return f"Function {function_name} not found."

            else:
                # Normal response
                assistant_message = response.choices[0].message.content
                self.conversation_history.append({"role": "assistant", "content": assistant_message})
                return assistant_message

        except Exception as e:
            return f"Error: {str(e)}"
```

## 4. Usage Examples

### Basic Usage
```python
# Initialize assistant
assistant = ChatAssistant()

# Add skills
assistant.add_skill("weather", weather_skill)
assistant.add_skill("code", code_assistant_skill)
assistant.add_skill("research", research_skill)

# Chat
print(assistant.process_message("Hello!"))
print(assistant.process_message("What's the weather in London?"))
print(assistant.process_message("Can you help me debug some Python code?"))
```

### Function Calling Usage
```python
# Initialize with functions
assistant = ChatAssistantWithFunctions()

# Define functions
assistant.add_function(
    name="calculate",
    description="Calculate mathematical expressions",
    parameters={
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "Mathematical expression to calculate"
            }
        },
        "required": ["expression"]
    }
)

# Add calculator function
def calculate(expression):
    try:
        result = eval(expression)
        return str(result)
    except:
        return "Invalid expression"

assistant.skills["calculate"] = calculate

# Use function calling
response = assistant.process_message_with_functions("What is 15 * 24?")
```

## 5. Testing the Assistant

### Unit Tests
```python
import unittest

class TestChatAssistant(unittest.TestCase):
    def setUp(self):
        self.assistant = ChatAssistant()

    def test_conversation_history(self):
        self.assistant.process_message("Hello")
        self.assertEqual(len(self.assistant.conversation_history), 2)

    def test_skill_activation(self):
        self.assistant.add_skill("test", lambda x, y: "Test response")
        response = self.assistant.process_message("Activate test skill")
        self.assertIn("Test response", response)

    def test_context_management(self):
        # Add many messages to trigger context management
        for i in range(20):
            self.assistant.process_message(f"Message {i}")
        self.assertLess(len(self.assistant.conversation_history), 25)
```

This implementation provides a comprehensive foundation for building chat applications with OpenAI's APIs, including skill management, context handling, and advanced features like function calling.