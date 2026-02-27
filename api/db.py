from sqlmodel import SQLModel, create_engine, Session
import os

# Import all models to register them with SQLModel
from models import User, Task, Conversation, Message

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create SQLModel engine
engine_params = {
    "echo": True,
    "pool_pre_ping": True,
}

# Only add pool_size and max_overflow for non-sqlite databases
if not DATABASE_URL.startswith("sqlite"):
    engine_params.update({
        "pool_size": 5,
        "max_overflow": 10
    })
else:
    # Special handling for SQLite
    engine_params["connect_args"] = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, **engine_params)

def get_session():
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    """Create database tables for all registered models"""
    SQLModel.metadata.create_all(engine)
