from .schemas import (
    AddTaskInput, AddTaskOutput,
    ListTasksInput, ListTasksOutput,
    CompleteTaskInput, CompleteTaskOutput,
    DeleteTaskInput, DeleteTaskOutput,
    UpdateTaskInput, UpdateTaskOutput
)
from .handlers import (
    add_task, list_tasks, complete_task,
    delete_task, update_task
)

TOOL_DEFINITIONS = [
    {
        "name": "add_task",
        "description": "Adds a new task to the user's todo list. Use this when the user wants to create a new task.",
        "input_schema": AddTaskInput,
        "output_schema": AddTaskOutput,
        "handler": add_task
    },
    {
        "name": "list_tasks",
        "description": "List the user's tasks with optional filtering. Shows all tasks if no filters are applied.",
        "input_schema": ListTasksInput,
        "output_schema": ListTasksOutput,
        "handler": list_tasks
    },
    {
        "name": "complete_task",
        "description": "Mark a task as complete or incomplete. Users can refer to tasks by ID or describe them.",
        "input_schema": CompleteTaskInput,
        "output_schema": CompleteTaskOutput,
        "handler": complete_task
    },
    {
        "name": "delete_task",
        "description": "Delete a task from the todo list. This action cannot be undone.",
        "input_schema": DeleteTaskInput,
        "output_schema": DeleteTaskOutput,
        "handler": delete_task
    },
    {
        "name": "update_task",
        "description": "Update a task's details including title, description, priority, category, or due date.",
        "input_schema": UpdateTaskInput,
        "output_schema": UpdateTaskOutput,
        "handler": update_task
    }
]
