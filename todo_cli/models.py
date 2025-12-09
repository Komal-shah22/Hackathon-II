import uuid
from typing import List, Optional
from datetime import datetime

class Task:
    """
    Represents a single To-Do task with various attributes.

    Attributes:
        id (str): A unique identifier for the task, automatically generated if not provided.
        description (str): A brief description of the task.
        completed (bool): True if the task is completed, False otherwise. Defaults to False.
        priority (Optional[int]): An optional integer representing the task's priority (e.g., 1 for high).
        due_date (Optional[datetime]): An optional datetime object indicating the task's due date.
        tags (Optional[List[str]]): An optional list of strings representing tags associated with the task.
    """
    def __init__(
        self,
        description: str,
        id: Optional[str] = None,
        completed: bool = False,
        priority: Optional[int] = None,
        due_date: Optional[datetime] = None,
        tags: Optional[List[str]] = None
    ):
        self.id = id if id is not None else str(uuid.uuid4())
        self.description = description
        self.completed = completed
        self.priority = priority
        self.due_date = due_date
        self.tags = tags if tags is not None else []

    def __repr__(self):
        status = "✓" if self.completed else " "
        priority_str = f" P{self.priority}" if self.priority is not None else ""
        due_date_str = f" due:{self.due_date.strftime('%Y-%m-%d')}" if self.due_date else ""
        tags_str = f" #{' #'.join(self.tags)}" if self.tags else ""
        return f"[{status}]{priority_str} {self.description}{due_date_str}{tags_str} (ID: {self.id[:4]}...)"

    def to_dict(self):
        """Converts the Task object to a dictionary for serialization."""
        return {
            "id": self.id,
            "description": self.description,
            "completed": self.completed,
            "priority": self.priority,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "tags": self.tags,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a Task object from a dictionary."""
        return cls(
            id=data["id"],
            description=data["description"],
            completed=data["completed"],
            priority=data.get("priority"),
            due_date=datetime.fromisoformat(data["due_date"]) if data.get("due_date") else None,
            tags=data.get("tags"),
        )
