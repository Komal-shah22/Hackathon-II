"""
MCP Tools Service

This module contains the implementation of MCP tools that can be used by AI agents
to interact with the todo application through natural language.
"""

from typing import Dict, Any, List
from sqlmodel import Session, select
from models import User, Task
from datetime import datetime


class MCPTaskTools:
    def __init__(self, db_session: Session):
        self.db = db_session

    def add_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new task"""
        user_id = params.get("user_id")
        title = params.get("title")
        description = params.get("description", "")

        if not user_id or not title:
            raise ValueError("user_id and title are required")

        # Verify user exists
        user = self.db.get(User, user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")

        # Create new task
        task = Task(
            user_id=user_id,
            title=title,
            description=description,
            completed=False
        )

        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)

        return {
            "task_id": task.id,
            "status": "created",
            "title": task.title
        }

    def list_tasks(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Retrieve tasks from the list"""
        user_id = params.get("user_id")
        status = params.get("status", "all")  # all, pending, completed

        if not user_id:
            raise ValueError("user_id is required")

        # Verify user exists
        user = self.db.get(User, user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")

        # Build query based on status
        query = select(Task).where(Task.user_id == user_id)

        if status == "pending":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)

        tasks = self.db.exec(query).all()

        return [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat() if task.created_at else None
            }
            for task in tasks
        ]

    def complete_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Mark a task as complete"""
        user_id = params.get("user_id")
        task_id = params.get("task_id")

        if not user_id or task_id is None:
            raise ValueError("user_id and task_id are required")

        # Verify user exists
        user = self.db.get(User, user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")

        # Find the task
        task = self.db.get(Task, task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")

        # Verify task belongs to user
        if task.user_id != user_id:
            raise ValueError(f"Task {task_id} does not belong to user {user_id}")

        # Update task completion
        task.completed = True
        task.updated_at = datetime.utcnow()
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)

        return {
            "task_id": task.id,
            "status": "completed",
            "title": task.title
        }

    def delete_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Remove a task from the list"""
        user_id = params.get("user_id")
        task_id = params.get("task_id")

        if not user_id or task_id is None:
            raise ValueError("user_id and task_id are required")

        # Verify user exists
        user = self.db.get(User, user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")

        # Find the task
        task = self.db.get(Task, task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")

        # Verify task belongs to user
        if task.user_id != user_id:
            raise ValueError(f"Task {task_id} does not belong to user {user_id}")

        # Delete the task
        self.db.delete(task)
        self.db.commit()

        return {
            "task_id": task_id,
            "status": "deleted",
            "title": task.title
        }

    def update_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Modify task title or description"""
        user_id = params.get("user_id")
        task_id = params.get("task_id")
        title = params.get("title")
        description = params.get("description")

        if not user_id or task_id is None:
            raise ValueError("user_id and task_id are required")

        if title is None and description is None:
            raise ValueError("At least one of title or description must be provided")

        # Verify user exists
        user = self.db.get(User, user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")

        # Find the task
        task = self.db.get(Task, task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")

        # Verify task belongs to user
        if task.user_id != user_id:
            raise ValueError(f"Task {task_id} does not belong to user {user_id}")

        # Update task details
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        task.updated_at = datetime.utcnow()

        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)

        return {
            "task_id": task.id,
            "status": "updated",
            "title": task.title
        }