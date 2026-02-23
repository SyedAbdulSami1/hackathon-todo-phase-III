import os
from dotenv import load_dotenv

# Load environment variables before importing other modules
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, tasks, chat
from db import create_db_and_tables
from contextlib import asynccontextmanager

# Initialize the agent instance to be reused
chat_agent = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    print("Starting up...")
    create_db_and_tables()

    # Initialize the chat agent
    from agents.factory import AgentFactory
    global chat_agent
    chat_agent = AgentFactory.create_default_agent()
    print("Chat agent initialized")

    yield

    # Shutdown
    print("Shutting down...")


app = FastAPI(
    title="Todo API",
    description="Backend API for Todo App",
    version="1.0.0",
    lifespan=lifespan,
    redirect_slashes=False
)

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    os.getenv("CORS_ORIGINS", "*"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use ["*"] for local development to avoid CORS issues
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(chat.router, prefix="/api", tags=["chat"])

@app.get("/")
async def root():
    return {"message": "Hello from the Todo Server!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Add a way to access the agent globally if needed
def get_chat_agent():
    """Get the global chat agent instance."""
    return chat_agent
