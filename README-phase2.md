# Todo Web App (Phase 2) - Full-Stack Professional Application

## Overview
This is a full-stack todo application built with Next.js 16 and FastAPI, featuring advanced task management capabilities and modern UI/UX design. This represents Phase 2 of the hackathon: "Full-Stack Web Application".

## Tech Stack
- **Frontend**: Next.js 16 (App Router), TypeScript, Tailwind CSS, Framer Motion, Shadcn UI
- **Backend**: FastAPI, Python 3.11+, SQLModel
- **Database**: PostgreSQL (Neon)
- **Authentication**: JWT with bcrypt password hashing

## Features Implemented in Phase 2

### Basic Features (P1 - Core Essentials)
- User authentication (signup, signin, logout)
- Create, read, update, delete tasks
- Mark tasks as complete/incomplete
- Protected routes with JWT verification

### Intermediate Features (P2 - Organization & Usability)
- Priority levels (High, Medium, Low)
- Categories (Work, Personal, Shopping, Health, Finance, Other)
- Search tasks by title and description
- Filter by status, priority, and category
- Sort by created date, due date, priority, or title

### Advanced Features (P3 - Intelligent Features)
- Due dates with date/time pickers
- Browser notification reminders
- Recurring tasks (daily, weekly, monthly)
- Task statistics dashboard with completion rates

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL database (Neon)

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Runs on http://localhost:3000

### Backend Setup
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

Runs on http://localhost:8000

## API Endpoints

### Authentication
- `POST /auth/signup` - Create new account
- `POST /auth/signin` - Sign in to account
- `POST /auth/logout` - Sign out
- `GET /auth/me` - Get current user

### Tasks
- `GET /api/{user_id}/tasks` - List tasks (with filters)
- `POST /api/{user_id}/tasks` - Create task
- `GET /api/{user_id}/tasks/{task_id}` - Get task
- `PUT /api/{user_id}/tasks/{task_id}` - Update task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete task
- `PATCH /api/{user_id}/tasks/{task_id}/complete` - Toggle completion

### Statistics
- `GET /api/{user_id}/stats` - Get user statistics

## Environment Variables

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@host:5432/db
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

## Project Structure
```
phase-2/
├── frontend/           # Next.js 16 application
│   ├── app/           # App Router pages
│   │   ├── (auth)/    # Auth pages (signin, signup)
│   │   └── (dashboard)/ # Dashboard pages
│   ├── components/    # React components
│   │   ├── auth/      # Auth components
│   │   ├── tasks/     # Task components
│   │   └── ui/        # UI primitives
│   └── lib/           # Utilities and API client
├── backend/           # FastAPI application
│   ├── routes/        # API endpoints
│   ├── models.py      # SQLModel definitions
│   ├── schemas.py     # Pydantic schemas
│   └── db.py          # Database connection
└── specs/             # Feature specifications
```

## Development

This project uses Spec-Driven Development (SDD) with Spec-Kit Plus:
1. `/sp.specify` - Create feature specification
2. `/sp.plan` - Design implementation approach
3. `/sp.tasks` - Generate task breakdown
4. `/sp.implement` - Execute implementation
5. `/sp.git.commit_pr` - Commit and create PR

## Phase 2 Completion
✅ **Phase 2: Full-Stack Web Application** - COMPLETE
- All Basic, Intermediate, and Advanced features implemented
- Full authentication system
- Task management with filtering, sorting, and search
- Statistics dashboard
- Modern UI with responsive design
- Database integration with PostgreSQL