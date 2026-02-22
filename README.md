# Full-Stack Todo Application with AI Chatbot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

A modern, full-stack Todo application built with Next.js for the frontend and FastAPI for the backend. It features user authentication, task management, an AI chatbot for natural language task management, and a clean, responsive UI.

## Features

- **User Authentication:** Secure user registration and login with JWT-based authentication.
- **Task Management:** Create, read, update, and delete tasks.
- **AI Chatbot:** Natural language interface to manage tasks using MCP tools.
- **Task Filtering:** Filter tasks by status (All, Pending, Completed).
- **Responsive UI:** A clean and modern user interface that works on all screen sizes.
- **Containerized:** Easily run the entire application with Docker Compose.

## Tech Stack

**Frontend:**
- [Next.js](https://nextjs.org/)
- [React](https://reactjs.org/)
- [TypeScript](https://www.typescriptlang.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Shadcn UI](https://ui.shadcn.com/)

**Backend:**
- [FastAPI](https://fastapi.tiangolo.com/)
- [Python](https://www.python.org/)
- [SQLModel](https://sqlmodel.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/) (with [Neon](https://neon.tech/))

**AI/ML:**
- [OpenAI API](https://platform.openai.com/) or [Anthropic API](https://www.anthropic.com/)
- [MCP Tools](https://modelcontextprotocol.dev/) for task management
- [React Context API](https://react.dev/learn/passing-data-deeply-with-context) for state management

**Tooling:**
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Alembic](https://alembic.sqlalchemy.org/) for database migrations

## Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) (v18 or later)
- [Python](https://www.python.org/) (v3.8 or later)
- [Docker](https://www.docker.com/get-started) (for Docker setup)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [YOUR_REPOSITORY_URL_HERE]
    cd hackathon-todo-phase-III # Or your repository name
    ```
    (Remember to replace `[YOUR_REPOSITORY_URL_HERE]` with your actual repository URL if you fork this project.)

2.  **Set up environment variables:**
    Create a `.env` file in the `backend` directory by copying the `.env.template` file.
    ```bash
    cp backend/.env.template backend/.env
    ```
    Update the `DATABASE_URL` in `backend/.env` with your Neon DB connection string.
    Add your OpenAI or Anthropic API key if you want to use the AI chatbot.

### Running the Application

There are two ways to run the application:

<details>
<summary><b>🚀 Using Docker (Recommended for Development)</b></summary>

This setup is optimized for local development with hot-reloading. It is not intended for production deployments.

1.  **Build and run the application:**
    ```bash
    docker-compose up --build
    ```

2.  **Access the application:**
    - Frontend: [http://localhost:3000](http://localhost:3000)
    - Backend: [http://localhost:8000](http://localhost:8000)

</details>

<details>
<summary><b>💻 Running Locally</b></summary>

**Backend:**

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run database migrations:**
    ```bash
    python migrate_db.py
    ```
    Or using Alembic:
    ```bash
    alembic upgrade head
    ```

5.  **Start the server:**
    ```bash
    uvicorn main:app --reload
    ```

**Frontend:**

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Start the development server:**
    ```bash
    npm run dev
    ```

</details>

## AI Chatbot Feature

The application includes an AI chatbot that allows users to manage their tasks using natural language. The chatbot supports:

- Creating tasks: "Add a task to buy groceries"
- Updating tasks: "Mark the meeting task as complete"
- Searching tasks: "Show me all pending tasks"
- Deleting tasks: "Delete the old project task"

The chatbot uses MCP (Model Context Protocol) tools to interact with the todo management system.

### Chat API Endpoints

- `POST /api/{user_id}/chat` - Process natural language requests
- `GET /api/{user_id}/conversations` - Get user's conversations
- `GET /api/{user_id}/conversations/{conversation_id}` - Get conversation history

## Project Structure

```
.
├── backend/                    # FastAPI backend
│   ├── Dockerfile
│   ├── main.py                 # Application entry point
│   ├── models.py               # Database models
│   ├── models/                 # Extended models (conversations, messages)
│   │   ├── conversation.py     # Conversation model
│   │   └── message.py          # Message model
│   ├── db.py                   # Database configuration
│   ├── routers/                # API routes
│   │   └── chat.py             # Chat API routes
│   ├── tools/                  # MCP tools
│   │   ├── base.py             # Base tool interface
│   │   ├── todo_create.py      # Create todo tool
│   │   ├── todo_update.py      # Update todo tool
│   │   ├── todo_delete.py      # Delete todo tool
│   │   ├── todo_search.py      # Search todo tool
│   │   ├── todo_complete.py    # Complete todo tool
│   │   └── registry.py         # Tool registry
│   ├── agents/                 # AI agent components
│   │   ├── config.py           # Agent configuration
│   │   ├── chat_agent.py       # Chat agent implementation
│   │   ├── tool_binder.py      # Tool binding logic
│   │   └── factory.py          # Agent factory
│   ├── services/               # Service layer
│   │   ├── conversation_service.py      # Conversation service
│   │   ├── message_service.py           # Message service
│   │   ├── conversation_loader.py       # Conversation loader
│   │   └── conversation_persistence.py  # Conversation persistence
│   ├── schemas/                # Pydantic schemas
│   │   ├── chat.py             # Chat schemas
│   │   └── history.py          # History schemas
│   ├── exceptions/             # Custom exceptions
│   │   └── chat.py             # Chat exceptions
│   ├── middleware/             # Middleware
│   │   └── error_handler.py    # Error handling middleware
│   ├── handlers/               # Event handlers
│   │   └── mcp_error_handler.py # MCP error handler
│   └── logging/                # Logging components
│       └── chat_logger.py      # Chat logging
├── frontend/                   # Next.js frontend
│   ├── Dockerfile
│   ├── app/
│   │   └── chat/               # Chat page
│   │       └── page.tsx        # Chat UI
│   ├── components/             # Reusable components
│   │   ├── ChatKitWrapper.tsx  # Chat UI component
│   │   └── Navigation.tsx      # Navigation component
│   ├── contexts/               # React contexts
│   │   └── ChatContext.tsx     # Chat context
│   ├── lib/                    # Utility functions
│   │   ├── api.ts              # API client
│   │   └── chat-api.ts         # Chat API client
│   └── ...
├── docker-compose.yml
└── README.md
```

## Environment Variables

### Backend
Create a `.env` file in the `backend` directory:
```env
DATABASE_URL=postgresql://...
JWT_SECRET=your-secret-key
OPENAI_API_KEY=your-openai-api-key  # Optional, for OpenAI integration
ANTHROPIC_API_KEY=your-anthropic-api-key  # Optional, for Anthropic integration
AGENT_MODEL_NAME=gpt-4  # Model to use for the agent
AGENT_PROVIDER=openai  # Provider for the agent (openai, anthropic, etc.)
NEXT_PUBLIC_CHAT_ENABLED=true  # Enable/disable chat feature
```

### Frontend
Create a `.env.local` file in the `frontend` directory:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_CHAT_ENABLED=true  # Enable/disable chat feature
```

## Database Migrations

The application uses Alembic for database migrations. To run migrations:

```bash
cd backend
alembic upgrade head
```

To create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
