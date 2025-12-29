---
description: FastAPI with SQLModel patterns, database operations, and REST API best practices. Use when building backend, creating APIs, database models, or when user mentions FastAPI, backend, API, or database.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Skill: FastAPI with SQLModel Patterns

This skill teaches Claude how to build FastAPI backends with SQLModel ORM, implement REST APIs, handle database operations, and follow Python best practices for the todo application.

---

## 1. PROJECT STRUCTURE

### Standard FastAPI Backend Structure

```
backend/
├── main.py                 # FastAPI app entry point
├── db.py                   # Database engine and session
├── models.py               # SQLModel table definitions
├── schemas.py              # Pydantic request/response schemas
├── auth.py                 # JWT verification utilities
├── config.py               # Settings and configuration
├── dependencies.py         # Shared dependencies
│
├── routes/                 # API route handlers
│   ├── __init__.py
│   ├── tasks.py            # Task CRUD endpoints
│   ├── users.py            # User-related endpoints
│   └── health.py           # Health check endpoint
│
├── services/               # Business logic layer
│   ├── __init__.py
│   └── task_service.py     # Task business operations
│
├── middleware/             # Custom middleware
│   ├── __init__.py
│   └── logging.py          # Request logging
│
├── tests/                  # Test files
│   ├── __init__.py
│   ├── conftest.py         # Pytest fixtures
│   ├── test_tasks.py
│   └── test_auth.py
│
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (git-ignored)
└── .env.example            # Template for env vars
```

### Key Conventions

- **main.py**: FastAPI app instance, middleware, router registration
- **models.py**: SQLModel table classes (database schema)
- **schemas.py**: Pydantic models for API request/response validation
- **db.py**: Database connection, engine, session management
- **routes/**: HTTP endpoint handlers (thin layer, delegates to services)
- **services/**: Business logic (reusable across routes)

---

## 2. FASTAPI APPLICATION SETUP

### Main Application Entry Point

```python
# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db import create_db_and_tables
from routes import tasks, health
from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup: Create database tables
    create_db_and_tables()
    yield
    # Shutdown: Cleanup resources if needed


app = FastAPI(
    title="Todo API",
    description="A production-ready Todo API built with FastAPI and SQLModel",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS Configuration - NEVER use allow_origins=["*"] in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # e.g., ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# Register routers
app.include_router(health.router, tags=["Health"])
app.include_router(tasks.router, prefix="/api", tags=["Tasks"])


@app.get("/")
async def root():
    return {"message": "Todo API is running", "docs": "/docs"}
```

### Configuration Management

```python
# config.py
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings from environment variables"""

    # Database
    DATABASE_URL: str

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    # JWT (for verification only - tokens issued by Better Auth)
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"

    # Application
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
```

### Environment Variables Template

```bash
# .env.example
DATABASE_URL=postgresql://user:password@host/database?sslmode=require
JWT_SECRET=your-secret-key-here
CORS_ORIGINS=["http://localhost:3000"]
DEBUG=false
```

---

## 3. SQLMODEL DATABASE MODELS

### Base Model Pattern

```python
# models.py
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Column, DateTime
from sqlalchemy import func


class TimestampMixin(SQLModel):
    """Mixin for created_at and updated_at timestamps"""
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False
        )
    )


class Task(TimestampMixin, table=True):
    """Task database model"""
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, nullable=False)
    title: str = Field(max_length=200, nullable=False)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, index=True)
    priority: int = Field(default=0, ge=0, le=5)  # 0-5 priority scale
    due_date: Optional[datetime] = Field(default=None)

    # Composite index for common queries
    class Config:
        # For SQLModel table classes
        pass


# Index definitions (alternative approach)
# from sqlalchemy import Index
# Index('idx_tasks_user_completed', Task.user_id, Task.completed)
```

### Model Relationships (if needed)

```python
# models.py - Extended with relationships
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    """User model (if storing users locally)"""
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    external_id: str = Field(unique=True, index=True)  # Better Auth user ID
    email: str = Field(unique=True, index=True)

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="owner")


class Task(TimestampMixin, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", index=True)
    title: str = Field(max_length=200, nullable=False)
    completed: bool = Field(default=False)

    # Relationship to user
    owner: Optional["User"] = Relationship(back_populates="tasks")
```

---

## 4. DATABASE CONNECTION AND SESSION

### Database Setup with Neon PostgreSQL

```python
# db.py
from sqlmodel import SQLModel, Session, create_engine
from config import settings

# Create engine with Neon PostgreSQL
# - pool_pre_ping: Check connection before using
# - pool_recycle: Recycle connections after 5 minutes (Neon timeout)
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Log SQL queries in debug mode
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={
        "sslmode": "require"  # Required for Neon
    }
)


def create_db_and_tables():
    """Create all database tables on startup"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependency for database session injection"""
    with Session(engine) as session:
        yield session
```

### Async Database Support (Optional)

```python
# db_async.py
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import settings

# Convert postgresql:// to postgresql+asyncpg://
async_database_url = settings.DATABASE_URL.replace(
    "postgresql://", "postgresql+asyncpg://"
)

async_engine = create_async_engine(
    async_database_url,
    echo=settings.DEBUG,
    pool_pre_ping=True,
)

async_session = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_async_session():
    """Dependency for async database session"""
    async with async_session() as session:
        yield session


async def create_db_and_tables_async():
    """Create tables asynchronously"""
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
```

---

## 5. PYDANTIC SCHEMAS

### Request/Response Schema Pattern

```python
# schemas.py
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


# ============ Task Schemas ============

class TaskBase(BaseModel):
    """Shared task properties"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: int = Field(default=0, ge=0, le=5)
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    """Schema for creating a task"""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating a task (all fields optional)"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None
    priority: Optional[int] = Field(None, ge=0, le=5)
    due_date: Optional[datetime] = None


class TaskResponse(TaskBase):
    """Schema for task in API responses"""
    id: int
    user_id: str
    completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TaskListResponse(BaseModel):
    """Schema for paginated task list"""
    items: List[TaskResponse]
    total: int
    page: int
    page_size: int
    has_more: bool


# ============ Common Schemas ============

class MessageResponse(BaseModel):
    """Generic message response"""
    message: str


class ErrorResponse(BaseModel):
    """Error response schema"""
    detail: str
    code: Optional[str] = None
```

---

## 6. JWT AUTHENTICATION

### JWT Verification (Tokens from Better Auth)

```python
# auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt.exceptions import PyJWTError
from config import settings

security = HTTPBearer()


class AuthError(HTTPException):
    """Custom authentication error"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )


def verify_jwt(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Verify JWT token and return user_id.

    Tokens are issued by Better Auth on the frontend.
    This function only verifies, never creates tokens.
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )

        user_id = payload.get("sub")
        if not user_id:
            raise AuthError("Token missing user identifier")

        return user_id

    except jwt.ExpiredSignatureError:
        raise AuthError("Token has expired")
    except jwt.InvalidTokenError as e:
        raise AuthError(f"Invalid token: {str(e)}")
    except PyJWTError:
        raise AuthError("Could not validate credentials")


def get_current_user(user_id: str = Depends(verify_jwt)) -> str:
    """Alias for verify_jwt for semantic clarity"""
    return user_id
```

### User Authorization Check

```python
# auth.py (continued)
from fastapi import Path


def authorize_user_access(
    user_id: str = Path(..., description="User ID from URL path"),
    auth_user_id: str = Depends(verify_jwt)
) -> str:
    """
    Verify the authenticated user matches the path user_id.
    Use as dependency when user_id is in the URL path.
    """
    if user_id != auth_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access another user's resources"
        )
    return auth_user_id
```

---

## 7. REST API ENDPOINTS

### Complete CRUD Router

```python
# routes/tasks.py
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select, col

from db import get_session
from models import Task
from schemas import (
    TaskCreate, TaskUpdate, TaskResponse,
    TaskListResponse, MessageResponse
)
from auth import verify_jwt, authorize_user_access

router = APIRouter()


# ============ List Tasks ============
@router.get(
    "/{user_id}/tasks",
    response_model=TaskListResponse,
    summary="List all tasks for a user"
)
async def list_tasks(
    user_id: str = Depends(authorize_user_access),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    session: Session = Depends(get_session)
):
    """Get all tasks for the authenticated user with optional filtering."""

    # Base query
    query = select(Task).where(Task.user_id == user_id)

    # Apply filters
    if completed is not None:
        query = query.where(Task.completed == completed)

    # Get total count
    count_query = select(Task).where(Task.user_id == user_id)
    if completed is not None:
        count_query = count_query.where(Task.completed == completed)
    total = len(session.exec(count_query).all())

    # Apply pagination and ordering
    query = (
        query
        .order_by(col(Task.created_at).desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )

    tasks = session.exec(query).all()

    return TaskListResponse(
        items=[TaskResponse.model_validate(t) for t in tasks],
        total=total,
        page=page,
        page_size=page_size,
        has_more=(page * page_size) < total
    )


# ============ Get Single Task ============
@router.get(
    "/{user_id}/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Get a single task"
)
async def get_task(
    task_id: int,
    user_id: str = Depends(authorize_user_access),
    session: Session = Depends(get_session)
):
    """Get a specific task by ID."""

    task = session.exec(
        select(Task)
        .where(Task.id == task_id)
        .where(Task.user_id == user_id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return TaskResponse.model_validate(task)


# ============ Create Task ============
@router.post(
    "/{user_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task"
)
async def create_task(
    task_data: TaskCreate,
    user_id: str = Depends(authorize_user_access),
    session: Session = Depends(get_session)
):
    """Create a new task for the authenticated user."""

    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        due_date=task_data.due_date
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return TaskResponse.model_validate(task)


# ============ Update Task ============
@router.put(
    "/{user_id}/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Update a task"
)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    user_id: str = Depends(authorize_user_access),
    session: Session = Depends(get_session)
):
    """Update an existing task."""

    task = session.exec(
        select(Task)
        .where(Task.id == task_id)
        .where(Task.user_id == user_id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update only provided fields
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    session.add(task)
    session.commit()
    session.refresh(task)

    return TaskResponse.model_validate(task)


# ============ Delete Task ============
@router.delete(
    "/{user_id}/tasks/{task_id}",
    response_model=MessageResponse,
    summary="Delete a task"
)
async def delete_task(
    task_id: int,
    user_id: str = Depends(authorize_user_access),
    session: Session = Depends(get_session)
):
    """Delete a task."""

    task = session.exec(
        select(Task)
        .where(Task.id == task_id)
        .where(Task.user_id == user_id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    session.delete(task)
    session.commit()

    return MessageResponse(message="Task deleted successfully")


# ============ Toggle Completion ============
@router.patch(
    "/{user_id}/tasks/{task_id}/complete",
    response_model=TaskResponse,
    summary="Toggle task completion"
)
async def toggle_task_completion(
    task_id: int,
    user_id: str = Depends(authorize_user_access),
    session: Session = Depends(get_session)
):
    """Toggle the completed status of a task."""

    task = session.exec(
        select(Task)
        .where(Task.id == task_id)
        .where(Task.user_id == user_id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    task.completed = not task.completed
    session.add(task)
    session.commit()
    session.refresh(task)

    return TaskResponse.model_validate(task)
```

### Health Check Endpoint

```python
# routes/health.py
from fastapi import APIRouter, Depends
from sqlmodel import Session, text
from db import get_session

router = APIRouter()


@router.get("/health")
async def health_check():
    """Basic health check"""
    return {"status": "healthy"}


@router.get("/health/db")
async def database_health(session: Session = Depends(get_session)):
    """Database connectivity check"""
    try:
        session.exec(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}
```

---

## 8. ERROR HANDLING

### Global Exception Handlers

```python
# main.py (add to existing)
from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)


@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handle database errors"""
    logger.error(f"Database error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Database error occurred", "code": "DATABASE_ERROR"}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors"""
    logger.exception(f"Unexpected error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "code": "INTERNAL_ERROR"}
    )
```

### Custom Exception Classes

```python
# exceptions.py
from fastapi import HTTPException, status


class NotFoundError(HTTPException):
    def __init__(self, resource: str = "Resource"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} not found"
        )


class ForbiddenError(HTTPException):
    def __init__(self, message: str = "Access denied"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message
        )


class ValidationError(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )


class ConflictError(HTTPException):
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=message
        )
```

---

## 9. MIDDLEWARE AND LOGGING

### Request Logging Middleware

```python
# middleware/logging.py
import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Log request
        logger.info(f"Request: {request.method} {request.url.path}")

        response = await call_next(request)

        # Log response
        process_time = time.time() - start_time
        logger.info(
            f"Response: {response.status_code} "
            f"({process_time:.3f}s)"
        )

        # Add timing header
        response.headers["X-Process-Time"] = str(process_time)

        return response
```

### Logging Configuration

```python
# logging_config.py
import logging
import sys

def setup_logging(debug: bool = False):
    """Configure application logging"""
    level = logging.DEBUG if debug else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    # Reduce noise from third-party libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.INFO if debug else logging.WARNING
    )
```

---

## 10. TESTING PATTERNS

### Pytest Configuration

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

from main import app
from db import get_session


@pytest.fixture(name="session")
def session_fixture():
    """Create in-memory database for testing"""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create test client with database override"""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers():
    """Generate valid auth headers for testing"""
    import jwt
    from config import settings

    token = jwt.encode(
        {"sub": "test-user-123"},
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )
    return {"Authorization": f"Bearer {token}"}
```

### Test Examples

```python
# tests/test_tasks.py
import pytest
from fastapi import status


def test_create_task(client, auth_headers):
    """Test creating a new task"""
    response = client.post(
        "/api/test-user-123/tasks",
        json={"title": "Test Task", "description": "A test task"},
        headers=auth_headers
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["completed"] is False


def test_list_tasks(client, auth_headers):
    """Test listing tasks"""
    # Create a task first
    client.post(
        "/api/test-user-123/tasks",
        json={"title": "Test Task"},
        headers=auth_headers
    )

    response = client.get(
        "/api/test-user-123/tasks",
        headers=auth_headers
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] >= 1


def test_unauthorized_access(client, auth_headers):
    """Test that users cannot access other users' tasks"""
    response = client.get(
        "/api/other-user-456/tasks",
        headers=auth_headers  # Token is for test-user-123
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_missing_auth(client):
    """Test that missing auth returns 401"""
    response = client.get("/api/test-user-123/tasks")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
```

---

## 11. BEST PRACTICES CHECKLIST

### Security

- [ ] JWT verification on ALL protected endpoints
- [ ] User authorization check (path user_id == token user_id)
- [ ] Input validation with Pydantic schemas
- [ ] SQL injection prevention (SQLModel parameterized queries)
- [ ] Environment variables for ALL secrets
- [ ] Explicit CORS origins (never `["*"]` in production)
- [ ] HTTPS required (enforce via Neon SSL)

### Database

- [ ] Index on foreign keys (user_id)
- [ ] Index on filter columns (completed)
- [ ] Index on sort columns (created_at)
- [ ] Connection pooling configured
- [ ] Timestamps on all tables
- [ ] Soft deletes if needed

### API Design

- [ ] RESTful URL patterns
- [ ] Proper HTTP status codes
- [ ] Consistent error response format
- [ ] Pagination for list endpoints
- [ ] Request/response schemas separate
- [ ] API versioning strategy

### Code Quality

- [ ] Type hints everywhere
- [ ] Dependency injection
- [ ] Business logic in services
- [ ] Thin route handlers
- [ ] Tests for all endpoints
- [ ] Logging for debugging

---

## 12. COMMON PATTERNS

### Bulk Operations

```python
@router.post("/{user_id}/tasks/bulk")
async def bulk_create_tasks(
    tasks: List[TaskCreate],
    user_id: str = Depends(authorize_user_access),
    session: Session = Depends(get_session)
):
    """Create multiple tasks at once"""
    created = []
    for task_data in tasks:
        task = Task(user_id=user_id, **task_data.model_dump())
        session.add(task)
        created.append(task)

    session.commit()
    for task in created:
        session.refresh(task)

    return [TaskResponse.model_validate(t) for t in created]
```

### Search with Full-Text

```python
@router.get("/{user_id}/tasks/search")
async def search_tasks(
    q: str = Query(..., min_length=2),
    user_id: str = Depends(authorize_user_access),
    session: Session = Depends(get_session)
):
    """Search tasks by title or description"""
    query = (
        select(Task)
        .where(Task.user_id == user_id)
        .where(
            col(Task.title).ilike(f"%{q}%") |
            col(Task.description).ilike(f"%{q}%")
        )
    )

    tasks = session.exec(query).all()
    return [TaskResponse.model_validate(t) for t in tasks]
```

### Soft Delete Pattern

```python
# models.py
class Task(TimestampMixin, table=True):
    # ... existing fields ...
    deleted_at: Optional[datetime] = Field(default=None)

# routes/tasks.py - Soft delete
@router.delete("/{user_id}/tasks/{task_id}")
async def soft_delete_task(task_id: int, ...):
    task.deleted_at = datetime.utcnow()
    session.add(task)
    session.commit()

# Filter out deleted in queries
query = select(Task).where(Task.deleted_at.is_(None))
```

---

## Quick Reference

| Component | Purpose |
|-----------|---------|
| `main.py` | App entry, middleware, routers |
| `models.py` | SQLModel table definitions |
| `schemas.py` | Pydantic request/response models |
| `db.py` | Database connection, sessions |
| `auth.py` | JWT verification |
| `routes/` | HTTP endpoint handlers |
| `services/` | Business logic |

| HTTP Status | Meaning |
|-------------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Validation error |
| 401 | Unauthorized (no/invalid token) |
| 403 | Forbidden (valid token, wrong user) |
| 404 | Not found |
| 500 | Server error |

---

## Execution

When this skill is invoked, Claude should:

1. **Analyze the request** to determine which FastAPI pattern applies
2. **Check existing code** for patterns and consistency
3. **Generate code** following the patterns above
4. **Apply security checks** on all endpoints (JWT + user authorization)
5. **Include proper typing** for all functions and models
6. **Add validation** with Pydantic schemas
7. **Follow the project structure** conventions

### Example Prompts

- "Create the FastAPI backend with task CRUD endpoints"
- "Set up SQLModel models for the todo application"
- "Add JWT authentication to all API routes"
- "Configure the database connection for Neon PostgreSQL"
- "Implement pagination for the task list endpoint"
- "Add search functionality to tasks"
