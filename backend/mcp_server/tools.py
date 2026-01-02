"""MCP tool definitions and registration."""
# REMOVE THIS LINE if it exists:
# from . import mcp_server  ❌ DELETE THIS

# Keep these imports (they're fine):
from mcp import Tool
from .handlers import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    update_task
)
from .schemas import (
    AddTaskInput,
    AddTaskOutput,
    ListTasksInput,
    ListTasksOutput,
    CompleteTaskInput,
    CompleteTaskOutput,
    DeleteTaskInput,
    DeleteTaskOutput,
    UpdateTaskInput,
    UpdateTaskOutput
)

# Change this function to ACCEPT server as parameter
def register_all_mcp_tools(server):
    """Register all 5 MCP tools with the provided server instance.
    
    Args:
        server: MCP Server instance (passed from __init__.py)
    
    Returns:
        The server instance with registered tools
    """
    
    # Register Tool 1: add_task
    @server.tool()
    async def add_task(input: AddTaskInput) -> AddTaskOutput:
        """Create a new task for the user."""
        return await handle_add_task(input)
    
    # Register Tool 2: list_tasks
    @server.tool()
    async def list_tasks(input: ListTasksInput) -> ListTasksOutput:
        """List user's tasks with optional filters."""
        return await handle_list_tasks(input)
    
    # Register Tool 3: complete_task
    @server.tool()
    async def complete_task(input: CompleteTaskInput) -> CompleteTaskOutput:
        """Mark a task as complete."""
        return await handle_complete_task(input)
    
    # Register Tool 4: delete_task
    @server.tool()
    async def delete_task(input: DeleteTaskInput) -> DeleteTaskOutput:
        """Delete a task."""
        return await handle_delete_task(input)
    
    # Register Tool 5: update_task
    @server.tool()
    async def update_task(input: UpdateTaskInput) -> UpdateTaskOutput:
        """Update task details."""
        return await handle_update_task(input)
    
    return server