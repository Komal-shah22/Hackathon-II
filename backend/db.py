import os
from sqlmodel import create_engine, Session, SQLModel

# Import your models here
from models import User, Task, Conversation, Message

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    'postgresql://neondb_owner:npg_rmJXS1K6anUh@ep-young-paper-a42jjvi2-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
)

# Create SQLModel engine
engine = create_engine(
    DATABASE_URL,
    echo=False
)


def get_session():
    """Dependency for FastAPI to get database session"""
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

def init_db():
    """Initialize database tables"""
    # This will create tables for all models that inherit from SQLModel
    SQLModel.metadata.create_all(engine)
    print("Database initialized successfully.")
