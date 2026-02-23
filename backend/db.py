from sqlmodel import SQLModel, create_engine, Session
import os

# Import all models to register them with SQLModel
# Handle different possible locations of the models
try:
    # Standard app import
    from .models import User as User_, Task as Task_  # Renamed to avoid conflicts
    from .models.conversation import Conversation
    from .models.message import Message
except ImportError:
    try:
        # Alternative import structure
        from models import User as User_, Task as Task_
        from models.conversation import Conversation
        from models.message import Message
    except ImportError:
        # For testing purposes when running from different contexts
        try:
            from backend.models import User as User_, Task as Task_
            from backend.models.conversation import Conversation
            from backend.models.message import Message
        except ImportError:
            # Last resort: import the base models only
            from .models import User as User_, Task as Task_

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create SQLModel engine
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries for development
    pool_pre_ping=True,  # Enable connection health checks
    pool_size=5,
    max_overflow=10
)

def get_session():
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    """Create database tables for all registered models"""
    SQLModel.metadata.create_all(engine)