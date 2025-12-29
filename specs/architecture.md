# Phase 2 Architecture

## System Architecture
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Next.js        │────▶│  FastAPI        │────▶│  Neon           │
│  Frontend       │     │  Backend        │     │  PostgreSQL     │
│  (Vercel)       │     │  (Railway)      │     │                 │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
       │                        │
       │                        │
       ▼                        ▼
  Better Auth              JWT Verification
  (Client)                 (Server)
```

## Components

### Frontend (Next.js 16)
- **Pages**: Home, Signin, Signup, Dashboard
- **Components**: TaskList, TaskItem, TaskForm, Layout, AuthGuard
- **Libraries**: Better Auth, Tailwind CSS
- **API Client**: Axios/Fetch with JWT handling

### Backend (FastAPI)
- **Models**: User (Better Auth), Task
- **Routes**: /api/{user_id}/tasks (CRUD endpoints)
- **Auth**: JWT verification middleware
- **Database**: SQLModel with Neon PostgreSQL

### Database Schema
```sql
-- Users table (managed by Better Auth)
users (
  id: string PK,
  email: string UNIQUE,
  name: string,
  created_at: timestamp
)

-- Tasks table
tasks (
  id: integer PK,
  user_id: string FK -> users.id,
  title: string NOT NULL,
  description: text,
  completed: boolean DEFAULT false,
  created_at: timestamp,
  updated_at: timestamp
)

-- Indexes
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
```

## Authentication Flow
1. User signs up → Better Auth creates user
2. User signs in → Better Auth generates JWT token
3. Frontend stores token
4. Frontend sends token in Authorization header
5. Backend verifies JWT and extracts user_id
6. Backend validates user_id matches request
7. Backend returns only user's data

## Security
- JWT tokens for authentication
- User isolation (filter all queries by user_id)
- CORS configured for frontend domain
- Environment variables for secrets
- HTTPS in production
