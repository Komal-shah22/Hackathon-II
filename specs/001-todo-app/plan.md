# Implementation Plan: Phase 2 Full-Stack Todo Application

**Branch**: `[001-todo-app]` | **Date**: 2025-12-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/sp.specify` with 7 user stories and 36 functional requirements

## Summary

Build a professional full-stack todo application with three-tier feature levels: Basic (Authentication, CRUD), Intermediate (Priority, Categories, Search, Filter, Sort), and Advanced (Due Dates, Reminders, Recurring Tasks, Statistics). Frontend uses Next.js 16 with Shadcn UI, backend uses FastAPI with SQLModel/Neon PostgreSQL, and authentication uses Better Auth with JWT.

## Technical Context

**Language/Version**: TypeScript 5.x (frontend), Python 3.11+ (backend)
**Primary Dependencies**: Next.js 16, FastAPI, SQLModel, Better Auth, Tailwind CSS, Shadcn UI
**Storage**: Neon PostgreSQL (serverless, SSL required) with SQLModel ORM
**Testing**: Jest/Vitest (frontend), pytest (backend)
**Target Platform**: Web browsers (Chrome, Firefox, Safari, Edge desktop)
**Project Type**: Full-stack web application (frontend + backend monorepo)
**Performance Goals**: CRUD operations < 10s, search/filter < 15s, UI responsive with 500+ tasks
**Constraints**: JWT auth on all protected routes, user data isolation, no hardcoded secrets
**Scale/Scope**: Single-user personal task management, ~1000 tasks per user expected

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Requirement | Status | Notes |
|-------------|--------|-------|
| All API endpoints require authentication | PASS | JWT verification on all `/api/*` routes except auth |
| User data isolation (filter by user_id) | PASS | All queries include `WHERE user_id = token.user_id` |
| No hardcoded secrets | PASS | Environment variables for all credentials |
| JWT tokens verified on every request | PASS | `auth.py` middleware validates Bearer tokens |
| Input validation at API boundaries | PASS | Pydantic models for all request/response data |
| CORS explicitly configured | PASS | Backend CORS with frontend origin only |
| TypeScript strict mode | PASS | Frontend `tsconfig.json` configured |
| Python type hints | PASS | All backend functions annotated |
| Next.js 16 with App Router | PASS | Frontend uses `app/` directory structure |
| FastAPI with async endpoints | PASS | Backend uses `async def` for all routes |
| SQLModel ORM | PASS | Models inherit from `SQLModel` class |
| REST API design | PASS | Standard HTTP methods and status codes |

**Gate Result**: PASS - All constitution requirements satisfied

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-app/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   ├── openapi.yaml     # OpenAPI 3.0 specification
│   └── schemas.yaml     # Reusable schema definitions
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
phase-2/
├── frontend/            # Next.js 16 application
│   ├── app/             # App Router pages and layouts
│   │   ├── (auth)/      # Authentication routes group
│   │   │   ├── signin/
│   │   │   └── signup/
│   │   ├── (dashboard)/ # Protected routes group
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx # /dashboard
│   │   ├── globals.css
│   │   └── layout.tsx   # Root layout
│   ├── components/      # Reusable UI components
│   │   ├── ui/          # Shadcn UI components
│   │   │   ├── button.tsx
│   │   │   ├── input.tsx
│   │   │   ├── modal.tsx
│   │   │   └── select.tsx
│   │   ├── tasks/       # Task-specific components
│   │   │   ├── TaskList.tsx
│   │   │   ├── TaskItem.tsx
│   │   │   ├── TaskForm.tsx
│   │   │   ├── TaskFilter.tsx
│   │   │   └── TaskStats.tsx
│   │   ├── layout/      # Layout components
│   │   │   ├── Header.tsx
│   │   │   └── Sidebar.tsx
│   │   └── auth/        # Auth components
│   │       └── AuthProvider.tsx
│   ├── lib/             # Utilities and API client
│   │   ├── api.ts       # API client with JWT handling
│   │   ├── hooks/       # Custom React hooks
│   │   │   ├── useTasks.ts
│   │   │   └── useAuth.ts
│   │   ├── utils.ts     # Utility functions
│   │   └── types.ts     # TypeScript type definitions
│   ├── package.json
│   └── tsconfig.json
│
├── backend/             # FastAPI application
│   ├── main.py          # Application entry point
│   ├── db.py            # Database connection and session
│   ├── models.py        # SQLModel database models
│   ├── schemas.py       # Pydantic schemas
│   ├── auth.py          # JWT verification middleware
│   ├── routes/          # API endpoint handlers
│   │   ├── __init__.py
│   │   ├── auth.py      # Authentication endpoints
│   │   └── tasks.py     # Task CRUD endpoints
│   ├── requirements.txt
│   └── .env.example
│
└── .env                 # Environment variables (not committed)
```

**Structure Decision**: Monorepo with `frontend/` (Next.js 16) and `backend/` (FastAPI) directories as per constitution. Each layer is independently deployable with clear separation of concerns.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | No violations | - |

---

## Phase 0: Research & Technical Decisions

### Technology Stack Confirmation

All technologies are specified in the constitution and user requirements:

| Layer | Technology | Source | Notes |
|-------|------------|--------|-------|
| Frontend Framework | Next.js 16 | Constitution | App Router required |
| Frontend Language | TypeScript 5.x | Constitution | Strict mode |
| Styling | Tailwind CSS | User input | Utility-first |
| UI Components | Shadcn UI | User input | Professional components |
| Backend Framework | FastAPI | Constitution | Async endpoints |
| Backend Language | Python 3.11+ | Constitution | Type hints required |
| ORM | SQLModel | Constitution | Hybrid Pydantic/SQLAlchemy |
| Database | Neon PostgreSQL | Constitution | Serverless, SSL |
| Auth | Better Auth + JWT | Constitution | HS256 signing |
| Notifications | Browser Notification API | User input | Native browser API |
| Deployment | Vercel + Railway | User input | Platform-specific |

### Key Technical Decisions

#### TD-001: Recurring Task Implementation

**Decision**: Create next occurrence on task completion (synchronous within completion handler)

**Rationale**:
- Immediate feedback for users
- No background job infrastructure needed
- Simpler deployment model
- Works within JWT request context

**Alternatives Considered**:
- Background job queue (Celery/RQ) - Rejected: Adds infrastructure complexity
- Scheduled cron job - Rejected: Less accurate timing, harder to debug

**Implementation**:
```python
@app.put("/tasks/{task_id}/complete")
async def complete_task(task_id: int, current_user: User = Depends(get_current_user)):
    task = await get_task_by_id(task_id, current_user.id)
    task.completed = True
    session.commit()

    if task.is_recurring:
        next_task = create_next_occurrence(task)
        session.add(next_task)

    session.commit()
    return task
```

#### TD-002: Reminder Notification Strategy

**Decision**: Client-side periodic polling with server-side reminder time storage

**Rationale**:
- Works when browser is open
- No WebSocket or service worker infrastructure
- Browser Notifications API integrates naturally
- Falls back to in-app notifications

**Implementation**:
- Server stores `reminder_time` on task
- Frontend checks for due reminders every 60 seconds
- When reminder triggers: show browser notification
- Mark `reminder_sent = True` after sending

#### TD-003: Search/Filter Strategy

**Decision**: Client-side filtering for normal lists (< 500 tasks), server-side for larger

**Rationale**:
- Real-time filtering requires < 100ms response
- 500 tasks is small for modern browsers
- Simplifies backend (single query endpoint)
- Better UX with instant feedback

**Implementation**:
```typescript
// Frontend: fetch all tasks once, filter locally
const { tasks } = useTasks();
const filteredTasks = useMemo(() => {
  return tasks.filter(t =>
    (!search || t.title.includes(search)) &&
    (!filter.priority || t.priority === filter.priority) &&
    // ... other filters
  );
}, [tasks, search, filter]);
```

#### TD-004: Statistics Aggregation

**Decision**: Database aggregation queries with cached counters

**Rationale**:
- Accurate counts without counting in application
- Efficient for large datasets
- Periodic cache invalidation for performance

**Implementation**:
```python
@app.get("/users/{user_id}/stats")
async def get_user_stats(user_id: int, current_user: User = Depends(get_current_user)):
    stats = session.exec(
        select([
            func.count(Task.id).label("total"),
            func.sum(case([(Task.completed == True, 1)], else_=0)).label("completed"),
            # ... more aggregations
        ]).where(Task.user_id == user_id)
    ).one()
    return stats
```

#### TD-005: State Management

**Decision**: React Context + useReducer for global state, useState for local

**Rationale**:
- No external state library needed (Redux/Zustand)
- Context provides separation of concerns
- useReducer handles complex updates (filter + sort + search)
- Simple debugging with React DevTools

**Implementation**:
```typescript
// TaskContext provides:
// - tasks: Task[]
// - filters: TaskFilters
// - searchQuery: string
// - dispatch: React.Dispatch<TaskAction>
```

---

## Phase 1: Data Model & Contracts

### Data Model

#### User Entity (Managed by Better Auth)

Better Auth manages users, but we need a reference:

```python
# backend/models.py
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
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

class Task(SQLModel, table=True):
    """
    Complete task entity with all fields from all feature levels.
    """
    __tablename__ = "tasks"

    # Basic fields (P1)
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)  # Better Auth user ID
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)

    # Intermediate fields (P2)
    priority: Optional[TaskPriority] = Field(default=None)
    category: Optional[TaskCategory] = Field(default=None)

    # Advanced fields (P3)
    due_date: Optional[datetime] = Field(default=None, index=True)
    reminder_time: Optional[datetime] = Field(default=None)
    reminder_sent: bool = Field(default=False)

    # Recurring task fields
    is_recurring: bool = Field(default=False)
    recurrence_pattern: Optional[RecurrencePattern] = Field(default=None)
    recurrence_interval: Optional[int] = Field(default=1)  # Every N days/weeks/months
    recurrence_days: Optional[str] = Field(default=None)  # JSON: ["Mon", "Wed", "Fri"]
    recurrence_end_date: Optional[datetime] = Field(default=None)
    parent_task_id: Optional[int] = Field(default=None, foreign_key="tasks.id")

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Self-referential relationship for recurring task series
    parent_task: Optional["Task"] = Relationship(
        back_populates="child_tasks",
        remote_side="Task.id"
    )
    child_tasks: List["Task"] = Relationship()


# Database indexes for performance
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_tasks_category ON tasks(category);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_created_at ON tasks(created_at);
```

### API Contracts

#### Authentication Endpoints

```yaml
# contracts/auth.yaml
openapi: 3.0.0
info:
  title: Todo App Auth API
  version: 1.0.0

paths:
  /auth/signup:
    post:
      summary: Create new user account
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [email, password]
              properties:
                email:
                  type: string
                  format: email
                password:
                  type: string
                  minLength: 8
      responses:
        201:
          description: Account created successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  user:
                    $ref: '#/components/schemas/User'
                  token:
                    type: string
                    description: JWT access token
        400:
          description: Invalid input or email already exists

  /auth/signin:
    post:
      summary: Authenticate user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [email, password]
              properties:
                email:
                  type: string
                  format: email
                password:
                  type: string
      responses:
        200:
          description: Login successful
          content:
            application/json:
              schema:
                type: object
                properties:
                  user:
                    $ref: '#/components/schemas/User'
                  token:
                    type: string
        401:
          description: Invalid credentials

  /auth/me:
    get:
      summary: Get current user profile
      security:
        - Bearer: []
      responses:
        200:
          description: User profile
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        401:
          description: Unauthorized

components:
  securitySchemes:
    Bearer:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    User:
      type: object
      properties:
        id:
          type: string
        email:
          type: string
          format: email
        created_at:
          type: string
          format: date-time
```

#### Task Endpoints

```yaml
# contracts/tasks.yaml
openapi: 3.0.0
info:
  title: Todo App Tasks API
  version: 1.0.0

paths:
  /tasks:
    get:
      summary: List all tasks for current user
      security:
        - Bearer: []
      parameters:
        - in: query
          name: status
          schema:
            type: string
            enum: [all, pending, completed]
        - in: query
          name: priority
          schema:
            type: string
            enum: [all, high, medium, low, none]
        - in: query
          name: category
          schema:
            type: string
            enum: [all, work, personal, shopping, health, finance, other]
        - in: query
          name: sort_by
          schema:
            type: string
            enum: [created_at, due_date, priority, title]
        - in: query
          name: sort_order
          schema:
            type: string
            enum: [asc, desc]
      responses:
        200:
          description: List of tasks
          content:
            application/json:
              schema:
                type: object
                properties:
                  tasks:
                    type: array
                    items:
                      $ref: '#/components/schemas/Task'
                  total:
                    type: integer

    post:
      summary: Create new task
      security:
        - Bearer: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateTaskRequest'
      responses:
        201:
          description: Task created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'

  /tasks/{task_id}:
    get:
      summary: Get single task
      security:
        - Bearer: []
      parameters:
        - in: path
          name: task_id
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Task details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        404:
          description: Task not found

    put:
      summary: Update task
      security:
        - Bearer: []
      parameters:
        - in: path
          name: task_id
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateTaskRequest'
      responses:
        200:
          description: Task updated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'

    delete:
      summary: Delete task
      security:
        - Bearer: []
      parameters:
        - in: path
          name: task_id
          required: true
          schema:
            type: integer
      responses:
        204:
          description: Task deleted

  /tasks/{task_id}/complete:
    put:
      summary: Toggle task completion
      security:
        - Bearer: []
      parameters:
        - in: path
          name: task_id
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                completed:
                  type: boolean
      responses:
        200:
          description: Task completion toggled
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
                properties:
                  next_occurrence:
                    $ref: '#/components/schemas/Task'
                    description: Created if task was recurring

  /users/{user_id}/stats:
    get:
      summary: Get user task statistics
      security:
        - Bearer: []
      parameters:
        - in: path
          name: user_id
          required: true
          schema:
            type: string
      responses:
        200:
          description: User statistics
          content:
            application/json:
              schema:
                type: object
                properties:
                  total_tasks:
                    type: integer
                  completed_tasks:
                    type: integer
                  completion_rate:
                    type: number
                    format: float
                  overdue_count:
                    type: integer
                  due_today_count:
                    type: integer
                  by_category:
                    type: object
                    additionalProperties:
                      type: integer
                  by_priority:
                    type: object
                    additionalProperties:
                      type: integer

components:
  schemas:
    Task:
      type: object
      properties:
        id:
          type: integer
        user_id:
          type: string
        title:
          type: string
        description:
          type: string
          nullable: true
        completed:
          type: boolean
        priority:
          type: string
          nullable: true
          enum: [high, medium, low, null]
        category:
          type: string
          nullable: true
          enum: [work, personal, shopping, health, finance, other, null]
        due_date:
          type: string
          format: date-time
          nullable: true
        reminder_time:
          type: string
          format: date-time
          nullable: true
        reminder_sent:
          type: boolean
        is_recurring:
          type: boolean
        recurrence_pattern:
          type: string
          nullable: true
          enum: [daily, weekly, monthly, null]
        recurrence_interval:
          type: integer
          nullable: true
        recurrence_days:
          type: string
          nullable: true
        recurrence_end_date:
          type: string
          format: date-time
          nullable: true
        parent_task_id:
          type: integer
          nullable: true
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time

    CreateTaskRequest:
      type: object
      required: [title]
      properties:
        title:
          type: string
          minLength: 1
          maxLength: 200
        description:
          type: string
          maxLength: 1000
          nullable: true
        priority:
          type: string
          enum: [high, medium, low, null]
          nullable: true
        category:
          type: string
          enum: [work, personal, shopping, health, finance, other, null]
          nullable: true
        due_date:
          type: string
          format: date-time
          nullable: true
        reminder_time:
          type: string
          format: date-time
          nullable: true
        is_recurring:
          type: boolean
          default: false
        recurrence_pattern:
          type: string
          enum: [daily, weekly, monthly, null]
          nullable: true
        recurrence_interval:
          type: integer
          minimum: 1
          nullable: true
        recurrence_days:
          type: string
          nullable: true
        recurrence_end_date:
          type: string
          format: date-time
          nullable: true

    UpdateTaskRequest:
      type: object
      properties:
        title:
          type: string
          minLength: 1
          maxLength: 200
        description:
          type: string
          maxLength: 1000
          nullable: true
        priority:
          type: string
          enum: [high, medium, low, null]
          nullable: true
        category:
          type: string
          enum: [work, personal, shopping, health, finance, other, null]
          nullable: true
        due_date:
          type: string
          format: date-time
          nullable: true
        reminder_time:
          type: string
          format: date-time
          nullable: true
        is_recurring:
          type: boolean
        recurrence_pattern:
          type: string
          enum: [daily, weekly, monthly, null]
          nullable: true
        recurrence_interval:
          type: integer
          minimum: 1
          nullable: true
        recurrence_days:
          type: string
          nullable: true
        recurrence_end_date:
          type: string
          format: date-time
          nullable: true
```

---

## Quickstart Guide

### Prerequisites

```bash
# Node.js 18+ for Next.js
node --version  # >= 18.0.0

# Python 3.11+ for FastAPI
python --version  # >= 3.11.0

# PostgreSQL client (for database migrations)
psql --version
```

### Environment Setup

```bash
# Clone and setup
git clone <repo>
cd phase-2

# Frontend setup
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local with your values

# Backend setup
cd ../backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your values
```

### Environment Variables

```bash
# frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000/api
BETTER_AUTH_URL=http://localhost:8000

# backend/.env
DATABASE_URL=postgresql://user:password@ep-xxx.us-east-1.aws.neon.tech/phase2?sslmode=require
SECRET_KEY=your-256-bit-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
FRONTEND_URL=http://localhost:3000
```

### Database Setup

```bash
# Backend: Create tables
cd backend
python -c "from db import create_tables; create_tables()"

# Or run migrations if using Alembic
alembic upgrade head
```

### Running the Application

```bash
# Terminal 1: Backend
cd backend
uvicorn main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev -- --port 3000
```

### Verify Installation

1. Open http://localhost:3000
2. Navigate to /signup
3. Create an account
4. Verify you see an empty task dashboard
5. Create a task and verify it appears

### Running Tests

```bash
# Frontend
cd frontend
npm test
npm run lint

# Backend
cd backend
pytest --cov
flake8 .
```

---

## Security Implementation

### JWT Verification Middleware

```python
# backend/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import Optional

security = HTTPBearer()

class TokenData(BaseModel):
    user_id: str
    email: Optional[str] = None
    exp: Optional[int] = None

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> TokenData:
    """Verify JWT and extract user data."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return TokenData(user_id=user_id, email=payload.get("email"))
    except JWTError:
        raise credentials_exception

def require_user_id(user_id_param: str, current_user: TokenData) -> str:
    """Ensure the requested user_id matches the authenticated user."""
    if user_id_param != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )
    return current_user.user_id
```

### Data Isolation Pattern

```python
# All database queries MUST filter by user_id
async def get_user_tasks(user_id: str, session) -> List[Task]:
    return session.exec(
        select(Task).where(Task.user_id == user_id)
    ).all()

async def get_task_by_id(task_id: int, user_id: str, session) -> Optional[Task]:
    return session.exec(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id
        )
    ).first()
```

### Input Validation

```python
# backend/schemas.py
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Optional[str] = Field(None, pattern="^(high|medium|low)$")
    category: Optional[str] = Field(None, pattern="^(work|personal|shopping|health|finance|other)$")
    due_date: Optional[datetime] = None
    # ... other fields

    @field_validator("due_date")
    @classmethod
    def due_date_not_in_past(cls, v: Optional[datetime]) -> Optional[datetime]:
        if v and v < datetime.utcnow():
            raise ValueError("Due date cannot be in the past")
        return v
```

### CORS Configuration

```python
# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],  # Only frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Implementation Phases Summary

### Phase 1: Foundation (P1 features)
1. Setup project structure (frontend + backend)
2. Configure database connection
3. Implement Better Auth signup/signin
4. JWT authentication middleware
5. Task CRUD API endpoints
6. Basic task list UI

### Phase 2: Organization (P2 features)
1. Priority system (UI + API)
2. Category system (UI + API)
3. Search functionality (client-side)
4. Filter system (status, priority, category)
5. Sort options
6. Enhanced UI with badges and indicators

### Phase 3: Advanced (P3 features)
1. Due date picker and storage
2. Overdue task highlighting
3. Browser notification setup
4. Reminder system
5. Recurring task logic
6. Statistics dashboard
7. Performance optimization

---

## Generated Artifacts

| Artifact | Path | Status |
|----------|------|--------|
| Plan | `specs/001-todo-app/plan.md` | Complete |
| Research | `specs/001-todo-app/research.md` | N/A - All tech specified |
| Data Model | `specs/001-todo-app/data-model.md` | See plan |
| Quickstart | `specs/001-todo-app/quickstart.md` | See plan |
| Contracts | `specs/001-todo-app/contracts/openapi.yaml` | Complete |
| Tasks | `specs/001-todo-app/tasks.md` | Run `/sp.tasks` |

---

## Next Steps

1. **Run `/sp.tasks`** to generate detailed task breakdown
2. **Run `/sp.implement`** to execute implementation through specialized agents
3. **Deploy frontend** to Vercel after Phase 1 completion
4. **Deploy backend** to Railway after Phase 1 completion
