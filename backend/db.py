import os
from sqlmodel import create_engine, Session, SQLModel

# Import your models here
from models import User, Task, Conversation, Message

# Use SQLite for local development, PostgreSQL for production
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./todo_app.db"  # Local SQLite database
)

# Create SQLModel engine
if DATABASE_URL.startswith("sqlite"):
    # SQLite doesn't support some features, so we disable them
    engine = create_engine(DATABASE_URL, echo=False)
else:
    # For PostgreSQL, we can use the full feature set
    engine = create_engine(DATABASE_URL, echo=False)

def get_session():
    """Dependency for FastAPI to get database session"""
    with Session(engine) as session:
        yield session

def init_db():
    """Initialize database tables"""
    # This will create tables for all models that inherit from SQLModel
    SQLModel.metadata.create_all(engine)
    print("Database initialized successfully.")
