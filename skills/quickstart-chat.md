# Quick Start: OpenAI Chat Skills Implementation

## 1. Setup

```bash
# Install required packages
pip install openai
pip install requests
pip install python-dotenv
```

## 2. Basic Implementation

### Create .env file
```env
OPENAI_API_KEY=your_openai_api_key_here
WEATHER_API_KEY=your_weather_api_key_here  # Optional
```

### Quick Start Code
```python
from skills.chat_skills_implementation import ChatAssistant

# Initialize assistant
assistant = ChatAssistant()

# Add ready-to-use skills
assistant.add_skill("weather", weather_skill)
assistant.add_skill("code", code_assistant_skill)
assistant.add_skill("research", research_skill)

# Start chatting
response = assistant.process_message("Hello! I need help with something.")
print(response)

# Example with weather
weather_response = assistant.process_message("What's the weather in Tokyo?")
print(weather_response)
```

## 3. Custom Skills

### Add your own skill
```python
def custom_skill(user_input: str, assistant: ChatAssistant) -> str:
    # Your skill logic here
    return "Custom response"

# Register the skill
assistant.add_skill("custom", custom_skill)
```

## 4. Function Calling

```python
from skills.chat_skills_implementation import ChatAssistantWithFunctions

# Initialize with function support
func_assistant = ChatAssistantWithFunctions()

# Add a function
func_assistant.add_function(
    name="calculate",
    description="Calculate mathematical expressions",
    parameters={
        "type": "object",
        "properties": {
            "expression": {"type": "string", "description": "Math expression"}
        },
        "required": ["expression"]
    }
)

# Register function implementation
def calculate(expression):
    return str(eval(expression))

func_assistant.skills["calculate"] = calculate

# Use function calling
response = func_assistant.process_message_with_functions("What is 2 + 2?")
```

## 5. Advanced Features

### Streaming Responses
```python
def stream_response(user_input: str):
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_input}],
        stream=True
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="")
```

### Context Management
```python
# The assistant automatically manages context
# But you can manually intervene:
assistant.conversation_history = []  # Clear history
summary = assistant.get_conversation_summary()  # Get summary
```

## 6. Testing

```python
import unittest
from skills.chat_skills_implementation import TestChatAssistant

unittest.main()
```

## 7. Deployment Tips

1. **Environment Variables**: Use `.env` for API keys
2. **Error Handling**: Wrap API calls in try-catch blocks
3. **Rate Limits**: Implement retry logic for API limits
4. **Security**: Validate all user inputs
5. **Performance**: Use async operations for concurrent requests

## 8. Next Steps

1. Explore the manifest file for available skills
2. Check the implementation guide for advanced patterns
3. Add custom skills specific to your use case
4. Implement testing and monitoring
5. Deploy with proper error handling and logging