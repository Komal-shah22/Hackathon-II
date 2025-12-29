---
description: Implement REST API endpoints with FastAPI, JWT authentication, and CRUD operations.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Skill: API Router Builder

This skill invokes the **api-router** agent to implement REST API routes for the todo application.

### When to Use

- Creating REST API endpoint handlers
- Implementing CRUD operations for resources
- Adding JWT authentication to routes
- Setting up request/response validation
- Implementing user authorization checks
- Creating API route structure

### Execution

**Invoke the api-router agent** with the user's request to:

1. Read API specifications from `specs/api/rest-endpoints.md` if available
2. Verify database models and auth dependencies exist
3. Create route files with complete implementation
4. Apply JWT verification to all protected endpoints
5. Implement user authorization checks
6. Register routers in main.py

### Required Endpoints (Todo Application)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/{user_id}/tasks | List tasks with status filter |
| POST | /api/{user_id}/tasks | Create new task |
| GET | /api/{user_id}/tasks/{id} | Get single task |
| PUT | /api/{user_id}/tasks/{id} | Update task |
| DELETE | /api/{user_id}/tasks/{id} | Delete task |
| PATCH | /api/{user_id}/tasks/{id}/complete | Toggle completion |

### Security Pattern (Applied to ALL Endpoints)

```python
@router.get("/{user_id}/tasks")
async def list_tasks(
    user_id: str,
    auth_user_id: str = Depends(verify_jwt),
    session: Session = Depends(get_session)
):
    # ALWAYS validate user authorization FIRST
    if user_id != auth_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access another user's tasks"
        )
    # Then proceed with database operation
```

### HTTP Status Codes

- **200**: Successful operation
- **201**: Resource created
- **400**: Validation error
- **401**: Invalid/missing JWT token
- **403**: Valid token but not authorized
- **404**: Resource not found

### Quality Checklist

- JWT verification on ALL endpoints
- User ID validation (path vs token) on ALL endpoints
- Proper HTTP status codes
- Response models for type safety
- Request validation with Pydantic
- Database queries filter by user_id
- Router registered in main.py

### Example Prompts

- "Create the REST API endpoints for tasks"
- "Set up the task endpoints with JWT auth"
- "Add proper user validation to all routes"
- "Implement the CRUD operations for todos"
- "Create the API route structure"
