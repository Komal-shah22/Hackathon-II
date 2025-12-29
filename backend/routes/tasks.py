from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select, func, case
from sqlmodel import Session

from models import Task
from schemas import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskListResponse,
    MessageResponse,
    UserStats,
)
from routes.auth import get_current_user_id
from db import get_session


router = APIRouter(prefix="/api", tags=["tasks"])


def apply_filters(query, user_id: str, status: str, priority: str, category: str, search: str):
    """Apply filters to task query"""
    # Base filter
    query = query.where(Task.user_id == user_id)

    # Status filter
    if status and status != "all":
        if status == "pending":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)

    # Priority filter
    if priority and priority != "all" and priority != "none":
        query = query.where(Task.priority == priority)
    elif priority == "none":
        query = query.where(Task.priority == None)

    # Category filter
    if category and category != "all":
        query = query.where(Task.category == category)

    # Search filter
    if search:
        search_term = f"%{search}%"
        query = query.where(
            (Task.title.ilike(search_term)) |
            (Task.description.ilike(search_term))
        )

    return query


@router.get("/{user_id}/tasks", response_model=TaskListResponse)
async def list_tasks(
    user_id: str,
    status: str = Query(default="all", description="Filter by status: all, pending, completed"),
    priority: str = Query(default="all", description="Filter by priority: all, high, medium, low, none"),
    category: str = Query(default="all", description="Filter by category"),
    search: str = Query(default="", description="Search in title and description"),
    sort_by: str = Query(default="created_at", description="Sort by: created_at, due_date, priority, title"),
    sort_order: str = Query(default="desc", description="Sort order: asc, desc"),
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(default=20, ge=1, le=100, description="Items per page (max 100)"),
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """List all tasks for a user with optional filters, search, sorting, and pagination"""
    # Verify user access
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Build query
    query = select(Task)

    # Apply filters
    query = apply_filters(query, user_id, status, priority, category, search)

    # Apply sorting
    if sort_by == "due_date":
        order_column = Task.due_date
    elif sort_by == "priority":
        # Custom priority ordering
        order_column = case(
            (Task.priority == "high", 1),
            (Task.priority == "medium", 2),
            (Task.priority == "low", 3),
            (Task.priority == None, 4),
            else_=5
        )
    elif sort_by == "title":
        order_column = Task.title
    else:  # created_at
        order_column = Task.created_at

    if sort_order == "asc":
        query = query.order_by(order_column.asc())
    else:
        query = query.order_by(order_column.desc())

    # Get total count before pagination
    count_query = select(func.count()).select_from(query.subquery())
    total = session.exec(count_query).one()

    # Calculate offset for pagination
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)

    # Execute query
    tasks = session.exec(query).all()

    # Calculate pagination metadata
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1

    return TaskListResponse(
        tasks=[TaskResponse.model_validate(t) for t in tasks],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )

@router.post("/{user_id}/tasks", response_model=TaskResponse, status_code=201)
async def create_task(
    user_id: str,
    task_data: TaskCreate,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """Create a new task with all fields"""
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        category=task_data.category,
        due_date=task_data.due_date,
        reminder_time=task_data.reminder_time,
        is_recurring=task_data.is_recurring,
        recurrence_pattern=task_data.recurrence_pattern,
        recurrence_interval=task_data.recurrence_interval,
        recurrence_days=task_data.recurrence_days,
        recurrence_end_date=task_data.recurrence_end_date,
        completed=False,
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return TaskResponse.model_validate(task)


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: str,
    task_id: int,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """Get a specific task"""
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return TaskResponse.model_validate(task)


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: str,
    task_id: int,
    task_data: TaskUpdate,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """Update a task with all fields"""
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Update fields
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    task.updated_at = datetime.utcnow()

    session.commit()
    session.refresh(task)

    return TaskResponse.model_validate(task)


@router.delete("/{user_id}/tasks/{task_id}", response_model=MessageResponse)
async def delete_task(
    user_id: str,
    task_id: int,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """Delete a task"""
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    session.delete(task)
    session.commit()

    return MessageResponse(message="Task deleted successfully")


@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_complete(
    user_id: str,
    task_id: int,
    completed: bool = True,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """Toggle task completion status"""
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Toggle or set completion
    task.completed = completed
    task.updated_at = datetime.utcnow()

    session.commit()
    session.refresh(task)

    return TaskResponse.model_validate(task)


@router.get("/{user_id}/stats", response_model=UserStats)
async def get_user_stats(
    user_id: str,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """Get user task statistics"""
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_ago = now.replace(hour=0, minute=0, second=0, microsecond=0)

    # Total tasks
    total_query = select(func.count()).where(Task.user_id == user_id)
    total_tasks = session.exec(total_query).one()

    # Completed tasks
    completed_query = select(func.count()).where(
        Task.user_id == user_id,
        Task.completed == True
    )
    completed_tasks = session.exec(completed_query).one()

    # Pending tasks
    pending_tasks = total_tasks - completed_tasks

    # Completion rate
    completion_rate = completed_tasks / total_tasks if total_tasks > 0 else 0.0

    # Overdue tasks (past due date, not completed)
    overdue_query = select(func.count()).where(
        Task.user_id == user_id,
        Task.due_date < now,
        Task.completed == False
    )
    overdue_count = session.exec(overdue_query).one()

    # Due today
    due_today_query = select(func.count()).where(
        Task.user_id == user_id,
        Task.due_date >= today_start,
        Task.due_date < today_start.replace(hour=23, minute=59, second=59),
        Task.completed == False
    )
    due_today_count = session.exec(due_today_query).one()

    # By category
    by_category = {}
    for cat in ["work", "personal", "shopping", "health", "finance", "other"]:
        cat_query = select(func.count()).where(
            Task.user_id == user_id,
            Task.category == cat
        )
        by_category[cat] = session.exec(cat_query).one()

    # By priority
    by_priority = {}
    for pri in ["high", "medium", "low"]:
        pri_query = select(func.count()).where(
            Task.user_id == user_id,
            Task.priority == pri
        )
        by_priority[pri] = session.exec(pri_query).one()

    return UserStats(
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        completion_rate=round(completion_rate, 2),
        overdue_count=overdue_count,
        due_today_count=due_today_count,
        by_category=by_category,
        by_priority=by_priority,
    )
