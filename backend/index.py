import os
import sys
from dotenv import load_dotenv

# Ensure the backend directory is in the Python path
# This solves import issues on some environments like Vercel
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Load environment variables before importing other modules
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
try:
    from routers import auth, tasks, chat
    from db import create_db_and_tables
    from agents.factory import AgentFactory
except ImportError as e:
    print(f"IMPORT ERROR in index.py: {str(e)}")
    import traceback
    traceback.print_exc()
    raise e

# Initialize the agent instance to be reused
chat_agent = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    print("Starting up...")
    try:
        create_db_and_tables()
        print("Database tables verified/created")
    except Exception as e:
        print(f"Database initialization error: {e}")

    # Initialize the chat agent safely
    global chat_agent
    try:
        chat_agent = AgentFactory.create_default_agent()
        print("Chat agent initialized")
    except Exception as e:
        print(f"Chat agent initialization error: {e}")
        chat_agent = None

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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
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

@app.get("/api/debug-env")
async def debug_env():
    google_key = os.getenv("GOOGLE_API_KEY")
    db_url = os.getenv("DATABASE_URL")
    return {
        "GOOGLE_API_KEY_PRESENT": google_key is not None,
        "GOOGLE_API_KEY_LENGTH": len(google_key) if google_key else 0,
        "GOOGLE_API_KEY_START": google_key[:5] if google_key else "None",
        "DATABASE_URL_PRESENT": db_url is not None,
        "PYTHON_PATH": sys.path
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Add a way to access the agent globally if needed
def get_chat_agent():
    """Get the global chat agent instance."""
    return chat_agent
