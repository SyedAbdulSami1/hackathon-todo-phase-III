# AI Chatbot Feature Documentation

## Overview

The AI Chatbot feature allows users to interact with the todo management system using natural language. The chatbot leverages MCP (Model Context Protocol) tools to perform various task management operations.

## Features

- Natural language task creation, update, deletion, and search
- Conversation history and persistence
- Context-aware responses
- MCP tool integration for task management
- User-specific conversations

## Architecture

### Backend Components

- **Models**: Conversation and Message entities for storing chat history
- **MCP Tools**: Specialized tools for todo operations (create, update, delete, search, complete)
- **Agent**: AI processing layer that interprets user requests and selects appropriate tools
- **Services**: Business logic layer for conversation and message management
- **Endpoints**: REST API for chat interactions

### Frontend Components

- **Chat Interface**: Real-time chat UI with conversation history
- **Context Management**: React Context for managing chat state
- **API Client**: Integration with backend chat API

## API Endpoints

### POST `/api/{user_id}/chat`

Process a natural language request and return an appropriate response.

**Request Body:**
```json
{
  "message": "Natural language request",
  "conversation_id": "Optional existing conversation ID"
}
```

**Response:**
```json
{
  "response": "AI response to the user",
  "conversation_id": "ID of the conversation",
  "message_id": "ID of the current message",
  "tool_used": "Name of MCP tool used",
  "actions_taken": ["List of actions performed"]
}
```

### GET `/api/{user_id}/conversations`

Get all conversations for a specific user.

**Response:**
```json
[
  {
    "id": "conversation ID",
    "title": "conversation title",
    "created_at": "ISO timestamp",
    "updated_at": "ISO timestamp"
  }
]
```

### GET `/api/{user_id}/conversations/{conversation_id}`

Get the history of a specific conversation.

**Response:**
```json
{
  "conversation_id": "ID of the conversation",
  "messages": [
    {
      "id": "message ID",
      "sender_type": "user|assistant|system",
      "content": "message content",
      "timestamp": "ISO timestamp",
      "tool_used": "tool name if applicable",
      "tool_result": "tool result if applicable"
    }
  ]
}
```

## MCP Tools

The chatbot integrates with the following MCP tools:

- `todo_create_tool`: Create new todo tasks
- `todo_update_tool`: Update existing todo tasks
- `todo_delete_tool`: Delete todo tasks
- `todo_search_tool`: Search/list existing tasks
- `todo_complete_tool`: Mark tasks as complete/incomplete

## Error Handling

The system implements comprehensive error handling:

- Custom chat exceptions
- MCP tool error handling
- User authorization validation
- Input validation
- Fallback responses for tool failures

## Configuration

The chatbot behavior can be configured through environment variables:

- `AGENT_MODEL_NAME`: The AI model to use (default: gpt-4)
- `AGENT_TEMPERATURE`: Creativity parameter (default: 0.7)
- `AGENT_PROVIDER`: AI provider (openai, anthropic, etc.)
- `ENABLE_MCP_TOOLS`: Enable/disable MCP tools (default: true)
- `MAX_HISTORY_MESSAGES`: Number of messages to include in context (default: 20)

## Development

### Adding New MCP Tools

1. Create a new tool class extending `BaseMCPTool`
2. Implement the required methods (`name`, `description`, `parameters`, `execute`)
3. Register the tool in the `MCPToolRegistry`

### Extending the Chat Agent

1. Modify the intent parsing logic in `ChatAgent._parse_intent`
2. Add new tool mappings as needed
3. Update the response generation logic if necessary

## Deployment

The chatbot feature is deployed as part of the main application. Ensure the following environment variables are set in production:

- `DATABASE_URL`: Properly configured database connection
- `JWT_SECRET`: Secure JWT secret
- `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`: Valid API key for the chosen provider
- `NEXT_PUBLIC_CHAT_ENABLED`: Enable/disable the chat UI (default: true)