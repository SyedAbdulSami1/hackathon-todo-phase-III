# Quickstart Guide: AI Chatbot for Natural Language Todo Management

## Overview
This guide will help you quickly set up and run the AI Chatbot feature for natural language todo management.

## Prerequisites
- Node.js 18+ (for frontend)
- Python 3.9+ (for backend)
- PostgreSQL or Neon database
- OpenAI or Anthropic API key (optional, for enhanced AI features)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd hackathon-todo-phase-III
```

### 2. Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Install Frontend Dependencies
```bash
cd ../frontend
npm install
```

### 4. Set Up Environment Variables
Create a `.env` file in the backend directory with the following variables:

```env
DATABASE_URL=<your-postgres-or-neon-database-url>
JWT_SECRET=<your-jwt-secret-key>
OPENAI_API_KEY=<your-openai-api-key-if-using-openai>  # Optional
ANTHROPIC_API_KEY=<your-anthropic-api-key-if-using-anthropic>  # Optional
NEXT_PUBLIC_CHAT_ENABLED=true
```

### 5. Run Database Migrations
```bash
cd backend
alembic upgrade head
```

### 6. Start the Backend Server
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### 7. Start the Frontend Server
```bash
cd frontend
npm run dev
```

## API Usage

### Making Chat Requests
Send a POST request to the chat endpoint:

```bash
curl -X POST http://localhost:8000/api/user123/chat \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add a task to buy milk",
    "conversation_id": "optional-existing-conversation-id"
  }'
```

## Development

### Running Tests
Backend tests:
```bash
cd backend
pytest
```

Frontend tests:
```bash
cd frontend
npm test
```

### Adding New MCP Tools
To add new MCP tools for additional functionality:

1. Create a new tool in the `backend/tools/` directory
2. Define the tool's schema and implementation
3. Register the tool with the agent system
4. Update the agent's tool selection logic if needed

### Database Schema Changes
Remember that all database changes must be additive-only to comply with the constitution. Use Alembic to create and run migrations:

```bash
# Create a new migration
alembic revision --autogenerate -m "Add new chatbot tables"

# Apply the migration
alembic upgrade head
```

## Troubleshooting

### Common Issues
- **JWT Authentication Errors**: Verify your JWT token is valid and has the correct user_id
- **Database Connection Issues**: Check that your DATABASE_URL is correctly configured
- **AI Service Errors**: Ensure your API keys are valid and have sufficient quota

### Debugging Tips
- Check the backend logs for detailed error messages
- Verify that all required environment variables are set
- Confirm that the database migrations have been applied