# Full-Stack Todo Application with AI Chatbot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

A modern, full-stack Todo application built with Next.js for the frontend and FastAPI for the backend. It features user authentication, task management, an AI chatbot for natural language task management, and a clean, responsive UI.

## ✨ Features

- **🔐 User Authentication:** Secure user registration and login with JWT-based authentication.
- **📝 Task Management:** Create, read, update, and delete tasks with status tracking.
- **🤖 AI Chatbot:** Natural language interface to manage tasks using MCP tools.
- **🔍 Smart Filtering:** Filter tasks by status (All, Pending, Completed).
- **📱 Responsive UI:** A clean and modern user interface that works on all screen sizes.
- **💬 Conversation History:** Persistent chat sessions with conversation history.
- **🔧 MCP Tool Integration:** State-of-the-art Model Context Protocol tools for task operations.
- **🐳 Containerized:** Easily run the entire application with Docker Compose.

## 🛠️ Tech Stack

**Frontend:**
- [Next.js](https://nextjs.org/) (App Router)
- [React](https://reactjs.org/)
- [TypeScript](https://www.typescriptlang.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Shadcn UI](https://ui.shadcn.com/)
- [ChatKit](https://github.com/chatkitlabs/chatkit) for chat interface

**Backend:**
- [FastAPI](https://fastapi.tiangolo.com/)
- [Python](https://www.python.org/) (v3.8+)
- [SQLModel](https://sqlmodel.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/) (with [Neon](https://neon.tech/))
- [Alembic](https://alembic.sqlalchemy.org/) for database migrations

**AI/ML & Tools:**
- [OpenAI API](https://platform.openai.com/) or [Anthropic API](https://www.anthropic.com/)
- [MCP Tools](https://modelcontextprotocol.dev/) for task management
- [LangChain](https://python.langchain.com/) for AI agent orchestration
- [React Context API](https://react.dev/learn/passing-data-deeply-with-context) for state management

**Tooling:**
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Vercel](https://vercel.com/) for frontend deployment

## 🚀 Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) (v18 or later)
- [Python](https://www.python.org/) (v3.8 or later)
- [Docker](https://www.docker.com/get-started) (for Docker setup)
- [Git](https://git-scm.com/)

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
    Configure the agent settings (model name and provider) as needed.

### Running the Application

There are two ways to run the application:

<details>
<summary><b>🐳 Using Docker (Recommended for Development)</b></summary>

This setup is optimized for local development with hot-reloading. It is not intended for production deployments.

1.  **Build and run the application:**
    ```bash
    docker-compose up --build
    ```

2.  **Access the application:**
    - Frontend: [http://localhost:3000](http://localhost:3000)
    - Backend: [http://localhost:8000](http://localhost:8000)
    - Chat Interface: [http://localhost:3000/chat](http://localhost:3000/chat)

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

4.  **Access the application:**
    - Frontend: [http://localhost:3000](http://localhost:3000)
    - Chat Interface: [http://localhost:3000/chat](http://localhost:3000/chat)

</details>

## 🤖 AI-Powered Chatbot Feature

The application includes an advanced AI chatbot that allows users to manage their tasks using natural language. The chatbot leverages MCP (Model Context Protocol) tools to provide intelligent task management capabilities:

- **📝 Create tasks:** "Add a task to buy groceries"
- **✅ Update tasks:** "Mark the meeting task as complete"
- **🔍 Search tasks:** "Show me all pending tasks"
- **🗑️ Delete tasks:** "Delete the old project task"
- **📚 Conversation History:** Persistent chat sessions with full conversation history
- **🔄 Context Awareness:** The AI remembers previous interactions and maintains context

The chatbot uses a sophisticated architecture with MCP tools to interact seamlessly with the todo management system, providing a natural language interface to your tasks.

### 📡 Chat API Endpoints

- `POST /api/{user_id}/chat` - Process natural language requests and manage tasks
- `GET /api/{user_id}/conversations` - Retrieve user's conversation history
- `GET /api/{user_id}/conversations/{conversation_id}` - Get specific conversation details
- `POST /api/{user_id}/conversations` - Start a new conversation

## 🏗️ Project Structure

```
.
├── backend/                          # FastAPI backend
│   ├── Dockerfile                    # Backend container configuration
│   ├── alembic/                      # Database migration scripts
│   │   ├── versions/                 # Individual migration files
│   │   │   ├── 0001_add_conversation_table.py  # Conversation table migration
│   │   │   └── 0002_add_message_table.py       # Message table migration
│   │   ├── env.py                    # Alembic environment
│   │   └── script.py.mako            # Migration template
│   ├── main.py                       # Application entry point
│   ├── models.py                     # Core database models
│   ├── models/                       # Extended models
│   │   ├── conversation.py           # Conversation model
│   │   └── message.py                # Message model
│   ├── db.py                         # Database configuration
│   ├── routers/                      # API route handlers
│   │   └── chat.py                   # Chat API routes
│   ├── tools/                        # MCP tools for AI integration
│   │   ├── base.py                   # Base tool interface
│   │   ├── todo_create.py            # Create todo tool
│   │   ├── todo_update.py            # Update todo tool
│   │   ├── todo_delete.py            # Delete todo tool
│   │   ├── todo_search.py            # Search todo tool
│   │   ├── todo_complete.py          # Complete todo tool
│   │   └── registry.py               # Tool registry
│   ├── agents/                       # AI agent components
│   │   ├── config.py                 # Agent configuration
│   │   ├── chat_agent.py             # Chat agent implementation
│   │   ├── tool_binder.py            # Tool binding logic
│   │   └── factory.py                # Agent factory
│   ├── services/                     # Business logic services
│   │   ├── conversation_service.py   # Conversation service
│   │   ├── message_service.py        # Message service
│   │   ├── conversation_loader.py    # Conversation loader
│   │   └── conversation_persistence.py # Conversation persistence
│   ├── schemas/                      # Pydantic data schemas
│   │   ├── chat.py                   # Chat request/response schemas
│   │   ├── history.py                # History schemas
│   │   └── errors.py                 # Error response schemas
│   ├── exceptions/                   # Custom exception classes
│   │   └── chat.py                   # Chat-specific exceptions
│   ├── middleware/                   # Request processing middleware
│   │   └── error_handler.py          # Error handling middleware
│   ├── handlers/                     # Event handlers
│   │   └── mcp_error_handler.py      # MCP error handler
│   └── logging/                      # Application logging
│       └── chat_logger.py            # Chat logging utilities
├── frontend/                         # Next.js frontend
│   ├── Dockerfile                    # Frontend container configuration
│   ├── app/                          # App Router pages
│   │   ├── chat/                     # Chat interface page
│   │   │   └── page.tsx              # Chat UI implementation
│   │   └── page.tsx                  # Main dashboard
│   ├── components/                   # Reusable UI components
│   │   ├── ChatKitWrapper.tsx        # ChatKit UI wrapper
│   │   └── Navigation.tsx            # Navigation component
│   ├── contexts/                     # React context providers
│   │   └── ChatContext.tsx           # Chat state management
│   ├── lib/                          # Utility functions
│   │   ├── api.ts                    # General API client
│   │   └── chat-api.ts               # Chat API client
│   ├── public/                       # Static assets
│   └── ...
├── docs/                             # Documentation
│   └── chat-feature.md               # Chat feature documentation
├── specs/                            # Specification files
│   └── ai-chatbot/                   # AI chatbot specs
├── docker-compose.yml                # Multi-container configuration
├── vercel.json                       # Vercel deployment configuration
└── README.md                         # This file
```

## 🔧 Environment Variables

### Backend
Create a `.env` file in the `backend` directory:
```env
# Database Configuration
DATABASE_URL=postgresql://...

# Authentication
JWT_SECRET=your-secret-key

# AI Provider Configuration
OPENAI_API_KEY=your-openai-api-key      # Required for OpenAI integration
ANTHROPIC_API_KEY=your-anthropic-api-key  # Required for Anthropic integration

# AI Agent Settings
AGENT_MODEL_NAME=gpt-4o                 # Model to use for the agent (gpt-4o, claude-3-sonnet, etc.)
AGENT_PROVIDER=openai                   # Provider for the agent (openai, anthropic)
NEXT_PUBLIC_CHAT_ENABLED=true           # Enable/disable chat feature

# Application Settings
LOG_LEVEL=INFO                          # Log level (DEBUG, INFO, WARNING, ERROR)
```

### Frontend
Create a `.env.local` file in the `frontend` directory:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_CHAT_ENABLED=true           # Enable/disable chat feature
NEXT_PUBLIC_BASE_URL=http://localhost:3000  # Base URL for the application
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

## 🤖 AI Agent Architecture

The AI chatbot is built using a modular architecture that separates concerns:

- **MCP Tools Layer**: Stateless tools that perform specific operations (create, update, delete, search, complete tasks)
- **Agent Layer**: AI agent that processes natural language and orchestrates tool usage
- **Service Layer**: Business logic for conversation management and persistence
- **Data Layer**: SQLModel entities for storing conversations and messages
- **Presentation Layer**: React components that provide a seamless chat experience

This architecture allows for easy extensibility and maintenance of the AI features.

## 📋 Development Workflow

The project follows a spec-driven development approach:

1. **Specification**: Define features in `/specs/` directory
2. **Implementation**: Build according to specifications
3. **Testing**: Validate against acceptance criteria
4. **Documentation**: Update documentation with new features

For the AI chatbot specifically, the development workflow includes:
1. Defining MCP tools in the `/backend/tools/` directory
2. Registering tools with the agent in the `/backend/agents/` directory
3. Testing tool functionality through the chat interface
4. Iterating on natural language understanding

## 🚀 Deployment

The application is designed for easy deployment:

- **Frontend**: Deploy to Vercel using the provided `vercel.json` configuration
- **Backend**: Deploy to any cloud provider supporting Python applications
- **Database**: Use Neon PostgreSQL for serverless scalability
- **Containerized**: Use Docker Compose for consistent environments

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
