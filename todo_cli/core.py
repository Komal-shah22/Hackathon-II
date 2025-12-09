from typing import List, Optional
from todo_cli.models import Task
from datetime import datetime

class TaskManager:
    """
    Manages the collection of To-Do tasks in-memory.

    Attributes:
        tasks (List[Task]): A list holding all the Task objects.
    """
    def __init__(self):
        self.tasks: List[Task] = []

    def add_task(self, description: str, priority: Optional[int] = None, due_date: Optional[datetime] = None, tags: Optional[List[str]] = None) -> Task:
        """Adds a new task to the in-memory list."""
        new_task = Task(description=description, priority=priority, due_date=due_date, tags=tags)
        self.tasks.append(new_task)
        return new_task

    def get_all_tasks(self, tag: Optional[str] = None, priority: Optional[int] = None, completed: Optional[bool] = None) -> List[Task]:
        """
        Returns all tasks in the in-memory list, optionally filtered by tag, priority, or completion status.
        """
        filtered_tasks = self.tasks

        if tag:
            filtered_tasks = [task for task in filtered_tasks if tag in task.tags]
        if priority is not None:
            filtered_tasks = [task for task in filtered_tasks if task.priority == priority]
        if completed is not None:
            filtered_tasks = [task for task in filtered_tasks if task.completed == completed]

        return filtered_tasks

    def search_tasks(self, query: str) -> List[Task]:
        """
        Searches for tasks whose descriptions contain the query string (case-insensitive).
        """
        return [task for task in self.tasks if query.lower() in task.description.lower()]

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """Returns a task by its ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(
        self,
        task_id: str,
        new_description: Optional[str] = None,
        completed: Optional[bool] = None,
        priority: Optional[int] = None,
        due_date: Optional[datetime] = None,
        tags: Optional[List[str]] = None
    ) -> Optional[Task]:
        """Updates an existing task."""
        task = self.get_task_by_id(task_id)
        if task:
            if new_description is not None:
                task.description = new_description
            if completed is not None:
                task.completed = completed
            if priority is not None:
                task.priority = priority
            if due_date is not None:
                task.due_date = due_date
            if tags is not None:
                task.tags = tags
            return task
        return None

    def delete_task(self, task_id: str) -> bool:
        """Deletes a task by its ID."""
        initial_len = len(self.tasks)
        self.tasks = [task for task in self.tasks if task.id != task_id]
        return len(self.tasks) < initial_len

# Initialize a global task manager for simplicity
task_manager = TaskManager()
