from . import mcp_server
from .handlers import add_task, list_tasks, complete_task, delete_task, update_task
from .schemas import (
    AddTaskInput, AddTaskOutput,
    ListTasksInput, ListTasksOutput,
    CompleteTaskInput, CompleteTaskOutput,
    DeleteTaskInput, DeleteTaskOutput,
    UpdateTaskInput, UpdateTaskOutput
)

# T023: Register all management tools with MCP server

@mcp_server.tool(
    name="add_task",
    description="Adds a new task to the user's todo list.",
    input_schema=AddTaskInput,
    output_schema=AddTaskOutput,
)
def add_task_tool(input: AddTaskInput, user_id: str) -> AddTaskOutput:
    return add_task(input, user_id)


@mcp_server.tool(
    name="list_tasks",
    description="Lists tasks with optional filtering.",
    input_schema=ListTasksInput,
    output_schema=ListTasksOutput,
)
def list_tasks_tool(input: ListTasksInput, user_id: str) -> ListTasksOutput:
    return list_tasks(input, user_id)


@mcp_server.tool(
    name="complete_task",
    description="Marks a task as complete or incomplete.",
    input_schema=CompleteTaskInput,
    output_schema=CompleteTaskOutput,
)
def complete_task_tool(input: CompleteTaskInput, user_id: str) -> CompleteTaskOutput:
    return complete_task(input, user_id)


@mcp_server.tool(
    name="delete_task",
    description="Deletes a task from the todo list.",
    input_schema=DeleteTaskInput,
    output_schema=DeleteTaskOutput,
)
def delete_task_tool(input: DeleteTaskInput, user_id: str) -> DeleteTaskOutput:
    return delete_task(input, user_id)


@mcp_server.tool(
    name="update_task",
    description="Updates a task's details.",
    input_schema=UpdateTaskInput,
    output_schema=UpdateTaskOutput,
)
def update_task_tool(input: UpdateTaskInput, user_id: str) -> UpdateTaskOutput:
    return update_task(input, user_id)


ALL_TOOLS = [
    "add_task",
    "list_tasks",
    "complete_task",
    "delete_task",
    "update_task",
]
