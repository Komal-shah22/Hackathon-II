from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr
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


class RecurrencePattern(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


# ============ User Schemas ============

class UserCreate(BaseModel):
    """Schema for creating a user"""
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    name: Optional[str] = Field(default=None, max_length=255)

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """Schema for user response"""
    id: str
    email: str
    name: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    """Schema for authentication response"""
    user: UserResponse
    token: str

    class Config:
        from_attributes = True


# ============ Task Schemas ============

class TaskBase(BaseModel):
    """Base schema for Task"""
    title: str = Field(max_length=200, min_length=1)
    description: Optional[str] = Field(default=None, max_length=1000)

    class Config:
        from_attributes = True


class TaskCreate(TaskBase):
    """Schema for creating a task"""
    priority: Optional[TaskPriority] = None
    category: Optional[TaskCategory] = None
    due_date: Optional[datetime] = None
    reminder_time: Optional[datetime] = None
    is_recurring: bool = False
    recurrence_pattern: Optional[RecurrencePattern] = None
    recurrence_interval: Optional[int] = Field(default=1, ge=1)
    recurrence_days: Optional[str] = None  # JSON array of day names
    recurrence_end_date: Optional[datetime] = None

    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    """Schema for updating a task"""
    title: Optional[str] = Field(default=None, max_length=200, min_length=1)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: Optional[TaskPriority] = None
    category: Optional[TaskCategory] = None
    due_date: Optional[datetime] = None
    reminder_time: Optional[datetime] = None
    is_recurring: Optional[bool] = None
    recurrence_pattern: Optional[RecurrencePattern] = None
    recurrence_interval: Optional[int] = Field(default=None, ge=1)
    recurrence_days: Optional[str] = None
    recurrence_end_date: Optional[datetime] = None
    completed: Optional[bool] = None

    class Config:
        from_attributes = True


class TaskResponse(TaskBase):
    """Schema for task response with all fields"""
    id: int
    user_id: str
    completed: bool
    priority: Optional[TaskPriority] = None
    category: Optional[TaskCategory] = None
    due_date: Optional[datetime] = None
    reminder_time: Optional[datetime] = None
    reminder_sent: bool = False
    is_recurring: bool = False
    recurrence_pattern: Optional[RecurrencePattern] = None
    recurrence_interval: Optional[int] = None
    recurrence_days: Optional[str] = None
    recurrence_end_date: Optional[datetime] = None
    parent_task_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """Schema for list of tasks with pagination"""
    tasks: List[TaskResponse]
    total: int
    page: int = 1
    page_size: int = 20
    total_pages: int = 1

    class Config:
        from_attributes = True


class TaskToggleComplete(BaseModel):
    """Schema for toggling task completion"""
    completed: bool


# ============ Statistics Schemas ============

class UserStats(BaseModel):
    """Schema for user statistics"""
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    completion_rate: float
    overdue_count: int
    due_today_count: int
    by_category: dict = {}
    by_priority: dict = {}

    class Config:
        from_attributes = True


# ============ Message Schemas ============

class MessageResponse(BaseModel):
    """Generic message response"""
    message: str

    class Config:
        from_attributes = True


# ============ Error Schemas ============

class ErrorResponse(BaseModel):
    """Error response schema"""
    detail: str
    code: Optional[str] = None

    class Config:
        from_attributes = True


# ============ Chatbot Schemas ============

class ChatRequest(BaseModel):
    """Request schema for chat endpoint"""
    conversation_id: Optional[int] = None
    message: str = Field(min_length=1, max_length=2000)

    class Config:
        from_attributes = True


class ToolCall(BaseModel):
    """Schema for representing a tool call made by the AI"""
    name: str
    arguments: dict

    class Config:
        from_attributes = True


class ChatResponse(BaseModel):
    """Response schema for chat endpoint"""
    conversation_id: int
    response: str
    tool_calls: List[ToolCall] = []

    class Config:
        from_attributes = True
