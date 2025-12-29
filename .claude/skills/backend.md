---
description: Build FastAPI backend infrastructure, database models, and API configuration for the todo application.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Skill: Backend Generator

This skill invokes the **backend-generator** agent to build FastAPI backend infrastructure for the todo application.

### When to Use

- Creating or modifying SQLModel database models
- Setting up database connections to Neon PostgreSQL
- Configuring CORS for frontend integration
- Adding JWT authentication middleware
- Implementing user isolation patterns
- Setting up the FastAPI application structure
- Adding Pydantic input validation

### Execution

**Invoke the backend-generator agent** with the user's request to:

1. Read API specifications from `specs/api/` if available
2. Check existing models and database configuration
3. Generate secure, production-ready FastAPI code
4. Implement proper authentication patterns
5. Apply user isolation for all data access
6. Configure CORS and middleware appropriately

### Output Expectations

The agent will:
- Create/modify files in `backend/` directory (main.py, models.py, db.py, auth.py, routes/)
- Use SQLModel for ORM with proper typing
- Implement JWT verification for protected routes
- Ensure all queries filter by user_id for data isolation
- Configure Neon PostgreSQL connection properly
- Never hardcode secrets (use environment variables)

### Security Requirements (Non-Negotiable)

1. JWT verification on all protected routes
2. User isolation in all database queries
3. SQL injection prevention via parameterized queries
4. Input validation through Pydantic models
5. Environment variables for all secrets
6. Explicit CORS origins (never allow_origins=["*"])

### Example Prompts

- "Set up the FastAPI backend with database models"
- "Add JWT authentication to all endpoints"
- "Configure CORS for the Next.js frontend"
- "Create the Todo model with proper indexes"
- "Implement user isolation for all routes"
