from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


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


# ============ Add Task Schemas ============

class AddTaskInput(BaseModel):
    title: str = Field(..., description="The title of the task.")
    description: Optional[str] = Field(None, description="A detailed description of the task.")


class AddTaskOutput(BaseModel):
    task_id: int = Field(..., description="The ID of the newly created task.")
    title: str = Field(..., description="The title of the created task.")
    status: str = Field("success", description="The status of the operation.")


# ============ List Tasks Schemas ============

class ListTasksInput(BaseModel):
    status: Optional[str] = Field(None, description="Filter by status: 'pending' or 'completed'")
    priority: Optional[TaskPriority] = Field(None, description="Filter by priority level")
    category: Optional[TaskCategory] = Field(None, description="Filter by category")
    search: Optional[str] = Field(None, description="Search in title and description")


class TaskListItem(BaseModel):
    id: int = Field(..., description="The unique identifier of the task.")
    title: str = Field(..., description="The title of the task.")
    description: Optional[str] = Field(None, description="The task description.")
    completed: bool = Field(..., description="Whether the task is completed.")
    priority: Optional[TaskPriority] = Field(None, description="Priority level.")
    category: Optional[TaskCategory] = Field(None, description="Category of the task.")
    due_date: Optional[datetime] = Field(None, description="Due date if set.")
    created_at: datetime = Field(..., description="When the task was created.")


class ListTasksOutput(BaseModel):
    tasks: List[TaskListItem] = Field(..., description="List of tasks matching the filters.")
    total_count: int = Field(..., description="Total number of tasks matching the filters.")
    status: str = Field("success", description="The status of the operation.")


# ============ Complete Task Schemas ============

class CompleteTaskInput(BaseModel):
    task_id: int = Field(..., description="The ID of the task to mark as complete.")
    completed: bool = Field(True, description="Whether to mark as complete (true) or incomplete (false).")


class CompleteTaskOutput(BaseModel):
    task_id: int = Field(..., description="The ID of the task that was updated.")
    completed: bool = Field(..., description="The new completion status.")
    title: str = Field(..., description="The title of the task.")
    status: str = Field("success", description="The status of the operation.")


# ============ Delete Task Schemas ============

class DeleteTaskInput(BaseModel):
    task_id: int = Field(..., description="The ID of the task to delete.")


class DeleteTaskOutput(BaseModel):
    task_id: int = Field(..., description="The ID of the deleted task.")
    title: str = Field(..., description="The title of the deleted task.")
    status: str = Field("success", description="The status of the operation.")


# ============ Update Task Schemas ============

class UpdateTaskInput(BaseModel):
    task_id: int = Field(..., description="The ID of the task to update.")
    title: Optional[str] = Field(None, description="New title for the task.")
    description: Optional[str] = Field(None, description="New description for the task.")
    priority: Optional[TaskPriority] = Field(None, description="New priority level.")
    category: Optional[TaskCategory] = Field(None, description="New category.")
    due_date: Optional[datetime] = Field(None, description="New due date.")


class UpdateTaskOutput(BaseModel):
    task_id: int = Field(..., description="The ID of the updated task.")
    title: str = Field(..., description="The updated title.")
    description: Optional[str] = Field(None, description="The updated description.")
    priority: Optional[TaskPriority] = Field(None, description="The updated priority.")
    category: Optional[TaskCategory] = Field(None, description="The updated category.")
    status: str = Field("success", description="The status of the operation.")
