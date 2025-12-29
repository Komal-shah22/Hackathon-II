from datetime import datetime
from typing import Optional, List
from enum import Enum
from sqlmodel import Field, SQLModel, Relationship


class User(SQLModel, table=True):
    """User account information"""
    __tablename__ = "users"

    id: str = Field(primary_key=True)
    email: str = Field(unique=True, index=True)
    name: Optional[str] = Field(default=None)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    tasks: List["Task"] = Relationship(back_populates="user")


class TaskPriority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskCategory(str, Enum):
    WORK = "work"
    PERSONAL = "personal"
    SHOPPING = "shopping"
    HEALTH = "health"
    FINANCE = "finance"
    OTHER = "other"


class RecurrencePattern(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class Task(SQLModel, table=True):
    """Complete task entity with all fields from all feature levels."""
    __tablename__ = "tasks"

    # Basic fields (P1)
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, foreign_key="users.id")
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, index=True)

    # Intermediate fields (P2)
    priority: Optional[TaskPriority] = Field(default=None, index=True)
    category: Optional[TaskCategory] = Field(default=None, index=True)

    # Advanced fields (P3)
    due_date: Optional[datetime] = Field(default=None, index=True)
    reminder_time: Optional[datetime] = Field(default=None)
    reminder_sent: bool = Field(default=False)

    # Recurring task fields
    is_recurring: bool = Field(default=False)
    recurrence_pattern: Optional[RecurrencePattern] = Field(default=None)
    recurrence_interval: Optional[int] = Field(default=1)  # Every N days/weeks/months
    recurrence_days: Optional[str] = Field(default=None)  # JSON: ["Mon", "Wed", "Fri"]
    recurrence_end_date: Optional[datetime] = Field(default=None)
    parent_task_id: Optional[int] = Field(default=None, foreign_key="tasks.id", index=True)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: Optional[User] = Relationship(back_populates="tasks")

    # Self-referential relationship for recurring task series
    parent_task: Optional["Task"] = Relationship(
        back_populates="child_tasks",
        sa_relationship_kwargs={"remote_side": "Task.id"}
    )
    child_tasks: List["Task"] = Relationship(back_populates="parent_task")

    class Config:
        from_attributes = True
