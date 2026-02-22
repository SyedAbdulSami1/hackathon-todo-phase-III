from dotenv import load_dotenv
load_dotenv()

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, tasks, chat
from db import create_db_and_tables

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
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (Local, Vercel, etc.)
    allow_credentials=False,  # Set to False to allow "*" wildcard (standard for Bearer tokens)
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(chat.router, prefix="/api", tags=["chat"])

@app.get("/")
async def root():
    return {"message": "Hello from the RELOADED Server!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Add a way to access the agent globally if needed
def get_chat_agent():
    """Get the global chat agent instance."""
    return chat_agent