---
description: Set up authentication with Better Auth frontend and FastAPI JWT backend verification.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Skill: Authentication Implementor

This skill invokes the **auth-implementor** agent to set up end-to-end authentication for the todo application.

### When to Use

- Setting up Better Auth on the frontend
- Creating login and signup pages
- Implementing JWT verification on the backend
- Securing API endpoints with authentication
- Setting up protected route wrappers
- Configuring session management
- Adding authorization checks

### Execution

**Invoke the auth-implementor agent** with the user's request to:

1. Configure Better Auth client setup
2. Create authentication pages (signin, signup)
3. Implement protected route layouts
4. Set up JWT verification in FastAPI
5. Update API client to include auth tokens
6. Apply security best practices throughout

### Frontend Responsibilities

- Auth client configuration in `lib/auth.ts`
- Signup page with validation at `app/(auth)/signup/page.tsx`
- Signin page with validation at `app/(auth)/signin/page.tsx`
- Protected layout that redirects unauthenticated users
- API client updates to include JWT tokens

### Backend Responsibilities

- JWT verification module in `auth.py`
- Route protection pattern using FastAPI dependencies
- User ID validation (path parameter vs token)
- Database query filtering by authenticated user

### Security Flow

```
1. User submits credentials → Better Auth validates
2. Better Auth generates JWT with user_id in 'sub' claim
3. Frontend stores token securely
4. Frontend includes token in Authorization header
5. Backend verifies signature with shared secret
6. Backend extracts and validates user_id
7. Backend returns only that user's data
```

### Critical Requirements

- `BETTER_AUTH_SECRET` must be identical on frontend and backend
- Always use `Authorization: Bearer <token>` format
- Validate URL user_id matches token user_id
- Filter all database queries by authenticated user_id

### Example Prompts

- "Set up authentication for the app"
- "Create the signup and signin pages"
- "Add JWT verification to the backend"
- "Implement protected routes for the dashboard"
- "Secure all API endpoints with authentication"
