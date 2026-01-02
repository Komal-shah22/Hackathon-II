import sys
sys.path.insert(0, 'backend')

from sqlmodel import Session, select
from mcp_server.schemas import (
    AddTaskInput, AddTaskOutput,
    ListTasksInput, ListTasksOutput, TaskListItem,
    CompleteTaskInput, CompleteTaskOutput,
    DeleteTaskInput, DeleteTaskOutput,
    UpdateTaskInput, UpdateTaskOutput
)
from models import Task
from db import get_session


content = '''from sqlmodel import Session, select
from .schemas import (
    AddTaskInput, AddTaskOutput,
    ListTasksInput, ListTasksOutput, TaskListItem,
    CompleteTaskInput, CompleteTaskOutput,
    DeleteTaskInput, DeleteTaskOutput,
    UpdateTaskInput, UpdateTaskOutput
)
from models import Task
from db import get_session


def add_task(input: AddTaskInput, user_id: str) -> AddTaskOutput:
    """
    T013: Adds a new task to the database for the given user.
    """
    with get_session() as session:
        db_task = Task(
            title=input.title,
            description=input.description,
            user_id=user_id
        )
        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        if db_task.id is None:
            raise Exception("Failed to create task")

        return AddTaskOutput(
            task_id=db_task.id,
            title=db_task.title
        )


def list_tasks(input: ListTasksInput, user_id: str) -> ListTasksOutput:
    """
    T020: List tasks for a user with optional filtering.
    """
    with get_session() as session:
        # Build the query with filters
        statement = select(Task).where(Task.user_id == user_id)

        # Apply status filter (pending = not completed)
        if input.status == "pending":
            statement = statement.where(Task.completed == False)
        elif input.status == "completed":
            statement = statement.where(Task.completed == True)

        # Apply priority filter
        if input.priority:
            statement = statement.where(Task.priority == input.priority)

        # Apply category filter
        if input.category:
            statement = statement.where(Task.category == input.category)

        # Apply search filter (title or description contains search term)
        if input.search:
            search_term = f"%{input.search}%"
            statement = statement.where(
                (Task.title.ilike(search_term)) |
                (Task.description.ilike(search_term))
            )

        # Order by created_at descending (most recent first)
        statement = statement.order_by(Task.created_at.desc())

        # Execute query
        tasks = session.exec(statement).all()

        # Convert to response format
        task_list = []
        for task in tasks:
            task_list.append(TaskListItem(
                id=task.id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                priority=task.priority,
                category=task.category,
                due_date=task.due_date,
                created_at=task.created_at
            ))

        return ListTasksOutput(
            tasks=task_list,
            total_count=len(task_list),
            status="success"
        )


def complete_task(input: CompleteTaskInput, user_id: str) -> CompleteTaskOutput:
    """
    T021: Mark a task as complete or incomplete.
    """
    with get_session() as session:
        # Get the task and verify ownership
        task = session.get(Task, input.task_id)
        if not task:
            raise ValueError(f"Task with ID {input.task_id} not found")
        if task.user_id != user_id:
            raise PermissionError("You do not have permission to modify this task")

        # Update the task
        task.completed = input.completed
        session.commit()
        session.refresh(task)

        return CompleteTaskOutput(
            task_id=task.id,
            completed=task.completed,
            title=task.title
        )


def delete_task(input: DeleteTaskInput, user_id: str) -> DeleteTaskOutput:
    """
    T022: Delete a task from the database.
    """
    with get_session() as session:
        # Get the task and verify ownership
        task = session.get(Task, input.task_id)
        if not task:
            raise ValueError(f"Task with ID {input.task_id} not found")
        if task.user_id != user_id:
            raise PermissionError("You do not have permission to delete this task")

        # Store title for response
        title = task.title

        # Delete the task
        session.delete(task)
        session.commit()

        return DeleteTaskOutput(
            task_id=input.task_id,
            title=title
        )


def update_task(input: UpdateTaskInput, user_id: str) -> UpdateTaskOutput:
    """
    T022: Update a task's details.
    """
    with get_session() as session:
        # Get the task and verify ownership
        task = session.get(Task, input.task_id)
        if not task:
            raise ValueError(f"Task with ID {input.task_id} not found")
        if task.user_id != user_id:
            raise PermissionError("You do not have permission to modify this task")

        # Update fields that were provided
        if input.title is not None:
            task.title = input.title
        if input.description is not None:
            task.description = input.description
        if input.priority is not None:
            task.priority = input.priority
        if input.category is not None:
            task.category = input.category
        if input.due_date is not None:
            task.due_date = input.due_date

        session.commit()
        session.refresh(task)

        return UpdateTaskOutput(
            task_id=task.id,
            title=task.title,
            description=task.description,
            priority=task.priority,
            category=task.category
        )
'''

with open('backend/mcp_server/handlers.py', 'w') as f:
    f.write(content)
print('File written successfully')
