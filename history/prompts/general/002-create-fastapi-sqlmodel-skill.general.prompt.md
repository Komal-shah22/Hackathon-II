---
id: 002
title: Create FastAPI SQLModel Custom Skill
stage: general
date: 2025-12-27
surface: agent
model: claude-sonnet-4.5
feature: none
branch: master
user: user
command: create skill
labels: ["skill", "fastapi", "sqlmodel", "backend", "documentation"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .claude/skills/fastapi-sqlmodel.md
tests:
  - none
---

## Prompt

Create a custom skill for my hackathon project Phase 2.

Skill Name: fastapi-sqlmodel

Purpose: This skill teaches Claude how to build FastAPI backends with SQLModel ORM, implement REST APIs, handle database operations, and follow Python best practices for the todo application.

When to use this skill:
- Building FastAPI backend
- Creating REST API endpoints
- Working with database models
- Implementing CRUD operations
- Setting up database connections
- User mentions "FastAPI", "backend", "API", "database", "SQLModel", or "Python"

Description for Claude to auto-detect:
"FastAPI with SQLModel patterns, database operations, and REST API best practices. Use when building backend, creating APIs, database models, or when user mentions FastAPI, backend, API, or database."

Key Topics to Cover:

1. PROJECT STRUCTURE

## Response snapshot

Created comprehensive FastAPI SQLModel skill file at `.claude/skills/fastapi-sqlmodel.md` covering:

1. **Project Structure** - Standard FastAPI backend folder layout (routes, services, middleware, tests)
2. **FastAPI Application Setup** - main.py with lifespan, CORS, router registration
3. **SQLModel Database Models** - TimestampMixin, Task model, relationships, indexes
4. **Database Connection** - Neon PostgreSQL setup, sync/async sessions, connection pooling
5. **Pydantic Schemas** - Request/response separation, validation, ConfigDict
6. **JWT Authentication** - Token verification, user authorization, security dependencies
7. **REST API Endpoints** - Complete CRUD router with pagination, filtering, authorization
8. **Error Handling** - Global exception handlers, custom exception classes
9. **Middleware and Logging** - Request logging middleware, logging configuration
10. **Testing Patterns** - Pytest fixtures, in-memory SQLite, auth headers
11. **Best Practices Checklist** - Security, database, API design, code quality
12. **Common Patterns** - Bulk operations, search, soft delete

## Outcome

- ✅ Impact: Created comprehensive skill file for FastAPI/SQLModel backend development guidance
- 🧪 Tests: None (documentation skill file)
- 📁 Files: 1 file created (.claude/skills/fastapi-sqlmodel.md)
- 🔁 Next prompts: Use skill for backend development, test with backend-generator agent
- 🧠 Reflection: Skill provides complete reference for secure FastAPI patterns specific to todo app

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A - documentation artifact
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Validate skill integration with backend-generator agent
