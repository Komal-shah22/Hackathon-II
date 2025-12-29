# Feature: User Authentication

## User Stories

### US1: User Registration
**As a** visitor
**I want to** create an account
**So that** I can access the todo app

**Acceptance Criteria:**
- User can enter email (valid format)
- User can enter password (min 8 chars)
- User can enter name (optional)
- Account created in database
- Success message shown
- Redirect to signin page

---

### US2: User Sign In
**As a** registered user
**I want to** sign in to my account
**So that** I can access my todos

**Acceptance Criteria:**
- User can enter email
- User can enter password
- JWT token returned on success
- Token stored securely (httpOnly cookie or secure storage)
- Redirect to dashboard
- Error message for invalid credentials

---

### US3: User Sign Out
**As a** logged-in user
**I want to** sign out
**So that** no one else can access my account

**Acceptance Criteria:**
- Token cleared from storage
- Redirect to signin page
- Cannot access protected routes after signout

---

### US4: Protected Routes
**As a** logged-out user
**I want to** be redirected when accessing protected pages
**So that** I cannot view private content without authentication

**Acceptance Criteria:**
- Dashboard redirects to signin if not logged in
- API calls without token return 401
- User cannot see other users' tasks

## Technical Implementation

### Frontend (Better Auth)
```typescript
// lib/auth.ts
import { createAuth } from "better-auth";

export const auth = createAuth({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  plugins: [],
});

// Sign up
const signUp = async (email: string, password: string, name: string) => {
  const data = await auth.signUp({
    email,
    password,
    name,
  });
  return data;
};

// Sign in
const signIn = async (email: string, password: string) => {
  const data = await auth.signIn({
    email,
    password,
  });
  return data;
};

// Sign out
const signOut = async () => {
  await auth.signOut();
};

// Get current session
const useSession = () => {
  const { data: session } = auth.useSession();
  return session;
};
```

### Backend (JWT Verification)
```python
# auth.py
from fastapi import HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from typing import Optional

security = HTTPBearer()
JWT_SECRET = "your-secret-key"  # From environment
JWT_ALGORITHM = "HS256"

async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_user(user_id: str = Depends(verify_token)) -> str:
    return user_id
```

## Environment Variables

### Frontend (.env.local)
```
BETTER_AUTH_SECRET=your-super-secret-key-at-least-32-characters-long
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend (.env)
```
JWT_SECRET=your-super-secret-key-at-least-32-characters-long
JWT_ALGORITHM=HS256
DATABASE_URL=postgresql://...
```

## Security Requirements
- Passwords hashed with bcrypt
- JWT tokens with expiration (24 hours)
- Secure HTTP-only cookies in production
- CORS configured for frontend origin
- No sensitive data in JWT payload (only user_id, email)
