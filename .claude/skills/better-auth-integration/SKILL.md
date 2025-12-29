---
description: Better Auth setup for Next.js frontend and FastAPI JWT verification. Use when implementing authentication, signup/signin, or when user mentions auth, Better Auth, JWT, or login.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Skill: Better Auth Integration

This skill teaches Claude how to implement Better Auth for Next.js frontend authentication and FastAPI backend JWT verification, ensuring secure end-to-end authentication flow for the todo application.

---

## 1. ARCHITECTURE OVERVIEW

### Authentication Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         AUTHENTICATION FLOW                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────┐         ┌──────────────┐         ┌──────────────┐     │
│  │   Browser    │         │   Next.js    │         │   FastAPI    │     │
│  │   (User)     │         │   Frontend   │         │   Backend    │     │
│  └──────┬───────┘         └──────┬───────┘         └──────┬───────┘     │
│         │                        │                        │              │
│         │  1. Enter credentials  │                        │              │
│         │───────────────────────>│                        │              │
│         │                        │                        │              │
│         │                 2. Better Auth                  │              │
│         │                    validates                    │              │
│         │                        │                        │              │
│         │  3. JWT token + cookie │                        │              │
│         │<───────────────────────│                        │              │
│         │                        │                        │              │
│         │  4. Request + JWT      │  5. Forward + JWT      │              │
│         │───────────────────────>│───────────────────────>│              │
│         │                        │                        │              │
│         │                        │  6. Verify JWT         │              │
│         │                        │     Extract user_id    │              │
│         │                        │     Check authorization│              │
│         │                        │                        │              │
│         │                        │  7. User's data only   │              │
│         │  8. Display data       │<───────────────────────│              │
│         │<───────────────────────│                        │              │
│         │                        │                        │              │
│  └──────────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility |
|-----------|----------------|
| **Better Auth (Frontend)** | User registration, login, session management, JWT issuance |
| **Next.js App** | Auth UI, protected routes, token storage, API calls |
| **FastAPI Backend** | JWT verification, user authorization, data isolation |

### Security Boundaries

```
Frontend Security:                    Backend Security:
├── Secure cookie storage             ├── JWT signature verification
├── HTTPS only                        ├── Token expiration check
├── CSRF protection                   ├── User ID validation
├── Protected route guards            ├── Data isolation per user
└── Token refresh handling            └── SQL injection prevention
```

---

## 2. BETTER AUTH SETUP (FRONTEND)

### Installation

```bash
npm install better-auth
```

### Auth Client Configuration

```typescript
// lib/auth-client.ts
import { createAuthClient } from "better-auth/react"

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000",
})

// Export typed hooks
export const {
  signIn,
  signUp,
  signOut,
  useSession,
  getSession,
} = authClient
```

### Auth Server Configuration

```typescript
// lib/auth.ts
import { betterAuth } from "better-auth"
import { Pool } from "pg"

export const auth = betterAuth({
  database: new Pool({
    connectionString: process.env.DATABASE_URL,
  }),

  emailAndPassword: {
    enabled: true,
    minPasswordLength: 8,
    maxPasswordLength: 128,
  },

  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24,     // Update session every 24 hours
    cookieCache: {
      enabled: true,
      maxAge: 60 * 5, // 5 minutes
    },
  },

  // JWT configuration - CRITICAL: must match backend
  jwt: {
    secret: process.env.BETTER_AUTH_SECRET!,
    expiresIn: 60 * 60 * 24, // 24 hours
  },

  // Rate limiting
  rateLimit: {
    window: 60,  // 60 seconds
    max: 10,     // 10 requests per window
  },
})

export type Session = typeof auth.$Infer.Session
```

### API Route Handler

```typescript
// app/api/auth/[...all]/route.ts
import { auth } from "@/lib/auth"
import { toNextJsHandler } from "better-auth/next-js"

export const { GET, POST } = toNextJsHandler(auth)
```

### Environment Variables

```bash
# .env.local (Next.js frontend)
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
DATABASE_URL=postgresql://user:password@host/database?sslmode=require

# CRITICAL: This secret MUST match the backend JWT_SECRET
BETTER_AUTH_SECRET=your-super-secret-key-at-least-32-characters-long
```

---

## 3. AUTHENTICATION PAGES

### Signup Page

```tsx
// app/(auth)/signup/page.tsx
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { signUp } from '@/lib/auth-client'

interface FormErrors {
  name?: string
  email?: string
  password?: string
  general?: string
}

export default function SignUpPage() {
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(false)
  const [errors, setErrors] = useState<FormErrors>({})

  const validateForm = (formData: FormData): FormErrors => {
    const errors: FormErrors = {}
    const name = formData.get('name') as string
    const email = formData.get('email') as string
    const password = formData.get('password') as string
    const confirmPassword = formData.get('confirmPassword') as string

    if (!name || name.length < 2) {
      errors.name = 'Name must be at least 2 characters'
    }

    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      errors.email = 'Please enter a valid email address'
    }

    if (!password || password.length < 8) {
      errors.password = 'Password must be at least 8 characters'
    }

    if (password !== confirmPassword) {
      errors.password = 'Passwords do not match'
    }

    return errors
  }

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setErrors({})

    const formData = new FormData(e.currentTarget)
    const validationErrors = validateForm(formData)

    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors)
      return
    }

    setIsLoading(true)

    try {
      const result = await signUp.email({
        name: formData.get('name') as string,
        email: formData.get('email') as string,
        password: formData.get('password') as string,
      })

      if (result.error) {
        setErrors({ general: result.error.message || 'Signup failed' })
        return
      }

      // Redirect to dashboard on success
      router.push('/todos')
      router.refresh()
    } catch (error) {
      setErrors({ general: 'An unexpected error occurred' })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-bold text-gray-900">
            Create your account
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Already have an account?{' '}
            <Link href="/signin" className="text-blue-600 hover:text-blue-500">
              Sign in
            </Link>
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {errors.general && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
              {errors.general}
            </div>
          )}

          <div className="space-y-4">
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                Full Name
              </label>
              <input
                id="name"
                name="name"
                type="text"
                required
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
              {errors.name && (
                <p className="mt-1 text-sm text-red-600">{errors.name}</p>
              )}
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                Email address
              </label>
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                required
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
              {errors.email && (
                <p className="mt-1 text-sm text-red-600">{errors.email}</p>
              )}
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="new-password"
                required
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700">
                Confirm Password
              </label>
              <input
                id="confirmPassword"
                name="confirmPassword"
                type="password"
                autoComplete="new-password"
                required
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
              {errors.password && (
                <p className="mt-1 text-sm text-red-600">{errors.password}</p>
              )}
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? 'Creating account...' : 'Create account'}
          </button>
        </form>
      </div>
    </div>
  )
}
```

### Signin Page

```tsx
// app/(auth)/signin/page.tsx
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { signIn } from '@/lib/auth-client'

export default function SignInPage() {
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setError('')
    setIsLoading(true)

    const formData = new FormData(e.currentTarget)
    const email = formData.get('email') as string
    const password = formData.get('password') as string

    try {
      const result = await signIn.email({
        email,
        password,
      })

      if (result.error) {
        setError(result.error.message || 'Invalid email or password')
        return
      }

      router.push('/todos')
      router.refresh()
    } catch (err) {
      setError('An unexpected error occurred')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-bold text-gray-900">
            Sign in to your account
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Don't have an account?{' '}
            <Link href="/signup" className="text-blue-600 hover:text-blue-500">
              Sign up
            </Link>
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}

          <div className="space-y-4">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                Email address
              </label>
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                required
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="current-password"
                required
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
          >
            {isLoading ? 'Signing in...' : 'Sign in'}
          </button>
        </form>
      </div>
    </div>
  )
}
```

### Auth Layout

```tsx
// app/(auth)/layout.tsx
import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'

export default async function AuthLayout({
  children,
}: {
  children: React.ReactNode
}) {
  // Check if user is already authenticated
  const cookieStore = await cookies()
  const session = cookieStore.get('better-auth.session_token')

  // Redirect authenticated users to dashboard
  if (session) {
    redirect('/todos')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {children}
    </div>
  )
}
```

---

## 4. PROTECTED ROUTES

### Protected Dashboard Layout

```tsx
// app/(dashboard)/layout.tsx
import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'
import { Sidebar } from '@/components/layout/sidebar'
import { Header } from '@/components/layout/header'

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const cookieStore = await cookies()
  const session = cookieStore.get('better-auth.session_token')

  // Redirect unauthenticated users to signin
  if (!session) {
    redirect('/signin')
  }

  return (
    <div className="min-h-screen flex">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <Header />
        <main className="flex-1 p-6 bg-gray-50">
          {children}
        </main>
      </div>
    </div>
  )
}
```

### useSession Hook Usage

```tsx
// components/layout/header.tsx
'use client'

import { useSession, signOut } from '@/lib/auth-client'
import { useRouter } from 'next/navigation'

export function Header() {
  const { data: session, isPending } = useSession()
  const router = useRouter()

  const handleSignOut = async () => {
    await signOut()
    router.push('/signin')
    router.refresh()
  }

  if (isPending) {
    return (
      <header className="h-16 border-b bg-white flex items-center justify-end px-6">
        <div className="animate-pulse bg-gray-200 h-8 w-24 rounded" />
      </header>
    )
  }

  return (
    <header className="h-16 border-b bg-white flex items-center justify-between px-6">
      <h1 className="text-xl font-semibold">Todo App</h1>

      <div className="flex items-center gap-4">
        <span className="text-sm text-gray-600">
          {session?.user?.email}
        </span>
        <button
          onClick={handleSignOut}
          className="text-sm text-gray-600 hover:text-gray-900"
        >
          Sign out
        </button>
      </div>
    </header>
  )
}
```

### Client-Side Route Protection (Alternative)

```tsx
// components/auth/require-auth.tsx
'use client'

import { useSession } from '@/lib/auth-client'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export function RequireAuth({ children }: { children: React.ReactNode }) {
  const { data: session, isPending } = useSession()
  const router = useRouter()

  useEffect(() => {
    if (!isPending && !session) {
      router.push('/signin')
    }
  }, [session, isPending, router])

  if (isPending) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
      </div>
    )
  }

  if (!session) {
    return null
  }

  return <>{children}</>
}
```

---

## 5. FASTAPI JWT VERIFICATION

### JWT Verification Module

```python
# backend/auth.py
from fastapi import Depends, HTTPException, status, Path
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt.exceptions import PyJWTError
from datetime import datetime
from typing import Optional
from config import settings

security = HTTPBearer()


class TokenPayload:
    """Parsed JWT token payload"""
    def __init__(self, user_id: str, email: Optional[str] = None, exp: Optional[int] = None):
        self.user_id = user_id
        self.email = email
        self.exp = exp


def verify_jwt(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Verify JWT token from Better Auth and return user_id.

    The token is issued by Better Auth on the frontend.
    We only verify the signature and extract the user_id.

    Returns:
        str: The user_id from the token's 'sub' claim

    Raises:
        HTTPException 401: If token is invalid, expired, or missing
    """
    token = credentials.credentials

    try:
        # Decode and verify the token
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,  # MUST match BETTER_AUTH_SECRET
            algorithms=[settings.JWT_ALGORITHM],
            options={
                "require": ["sub", "exp"],  # Required claims
                "verify_exp": True,
            }
        )

        # Extract user_id from 'sub' claim
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing user identifier",
                headers={"WWW-Authenticate": "Bearer"}
            )

        return user_id

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"}
        )

    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"}
        )

    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )


def authorize_user_access(
    user_id: str = Path(..., description="User ID from URL path"),
    auth_user_id: str = Depends(verify_jwt)
) -> str:
    """
    Verify the authenticated user has access to the requested resource.

    This dependency:
    1. Extracts user_id from URL path
    2. Gets authenticated user_id from JWT token
    3. Compares them to ensure user can only access their own data

    Usage:
        @router.get("/{user_id}/tasks")
        async def get_tasks(user_id: str = Depends(authorize_user_access)):
            # user_id is guaranteed to match the authenticated user

    Returns:
        str: The validated user_id

    Raises:
        HTTPException 403: If user_id doesn't match authenticated user
    """
    if user_id != auth_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access another user's resources"
        )

    return auth_user_id


def get_current_user(user_id: str = Depends(verify_jwt)) -> str:
    """Alias for verify_jwt with semantic naming"""
    return user_id
```

### Backend Configuration

```python
# backend/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str

    # JWT - MUST match BETTER_AUTH_SECRET on frontend
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
```

### Backend Environment Variables

```bash
# backend/.env
DATABASE_URL=postgresql://user:password@host/database?sslmode=require

# CRITICAL: This MUST match BETTER_AUTH_SECRET on the frontend
JWT_SECRET=your-super-secret-key-at-least-32-characters-long
JWT_ALGORITHM=HS256

CORS_ORIGINS=["http://localhost:3000"]
```

---

## 6. API CLIENT WITH AUTH

### Authenticated API Client

```typescript
// lib/api-client.ts
import { getSession } from '@/lib/auth-client'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface ApiError {
  detail: string
  code?: string
}

class ApiClient {
  private async getAuthHeaders(): Promise<HeadersInit> {
    const session = await getSession()

    if (!session?.data?.session?.token) {
      throw new Error('Not authenticated')
    }

    return {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${session.data.session.token}`,
    }
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const headers = await this.getAuthHeaders()

    const res = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers: {
        ...headers,
        ...options.headers,
      },
    })

    if (!res.ok) {
      const error: ApiError = await res.json().catch(() => ({
        detail: 'An error occurred',
      }))

      if (res.status === 401) {
        // Token expired or invalid - redirect to login
        if (typeof window !== 'undefined') {
          window.location.href = '/signin'
        }
      }

      throw new Error(error.detail)
    }

    return res.json()
  }

  // Task endpoints with user_id in path
  async getTasks(userId: string) {
    return this.request<Task[]>(`/api/${userId}/tasks`)
  }

  async getTask(userId: string, taskId: string) {
    return this.request<Task>(`/api/${userId}/tasks/${taskId}`)
  }

  async createTask(userId: string, data: CreateTaskInput) {
    return this.request<Task>(`/api/${userId}/tasks`, {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  async updateTask(userId: string, taskId: string, data: UpdateTaskInput) {
    return this.request<Task>(`/api/${userId}/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    })
  }

  async deleteTask(userId: string, taskId: string) {
    return this.request<void>(`/api/${userId}/tasks/${taskId}`, {
      method: 'DELETE',
    })
  }

  async toggleTaskComplete(userId: string, taskId: string) {
    return this.request<Task>(`/api/${userId}/tasks/${taskId}/complete`, {
      method: 'PATCH',
    })
  }
}

export const api = new ApiClient()
```

### Using API Client with Session

```tsx
// app/(dashboard)/todos/page.tsx
import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'
import { auth } from '@/lib/auth'
import { TodoList } from '@/components/todos/todo-list'

async function getTodos(userId: string, token: string) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/${userId}/tasks`, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    next: { revalidate: 0 }, // Always fetch fresh
  })

  if (!res.ok) {
    throw new Error('Failed to fetch todos')
  }

  return res.json()
}

export default async function TodosPage() {
  const cookieStore = await cookies()
  const sessionToken = cookieStore.get('better-auth.session_token')?.value

  if (!sessionToken) {
    redirect('/signin')
  }

  // Get session to extract user ID and JWT
  const session = await auth.api.getSession({
    headers: {
      cookie: `better-auth.session_token=${sessionToken}`,
    },
  })

  if (!session) {
    redirect('/signin')
  }

  const todos = await getTodos(session.user.id, session.session.token)

  return <TodoList initialTodos={todos} userId={session.user.id} />
}
```

---

## 7. SECURITY BEST PRACTICES

### Critical Security Checklist

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      SECURITY CHECKLIST                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ☐ Secrets Management                                                   │
│    ├── BETTER_AUTH_SECRET = JWT_SECRET (identical)                      │
│    ├── At least 32 characters long                                      │
│    ├── Never committed to git                                           │
│    └── Different per environment                                        │
│                                                                          │
│  ☐ Token Handling                                                       │
│    ├── Always use Authorization: Bearer <token>                         │
│    ├── Verify token signature on every request                          │
│    ├── Check token expiration                                           │
│    └── Handle refresh gracefully                                        │
│                                                                          │
│  ☐ User Authorization                                                   │
│    ├── Validate URL user_id matches token user_id                       │
│    ├── Filter ALL database queries by user_id                           │
│    ├── Never trust client-provided user_id                              │
│    └── Return 403 for authorization failures                            │
│                                                                          │
│  ☐ CORS Configuration                                                   │
│    ├── Explicit origins (never ["*"])                                   │
│    ├── allow_credentials: true for cookies                              │
│    └── Restrict methods to what's needed                                │
│                                                                          │
│  ☐ Cookie Security                                                      │
│    ├── HttpOnly: true (default in Better Auth)                          │
│    ├── Secure: true in production                                       │
│    ├── SameSite: Lax or Strict                                          │
│    └── Appropriate expiration                                           │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Secret Synchronization

```
CRITICAL: The authentication secret MUST be identical across systems

Frontend (.env.local):        Backend (.env):
BETTER_AUTH_SECRET=xyz   ══   JWT_SECRET=xyz

If these don't match:
- JWT verification will fail
- Users will get 401 errors
- Auth flow will be completely broken
```

### Common Security Mistakes

| Mistake | Fix |
|---------|-----|
| Different secrets frontend/backend | Use identical BETTER_AUTH_SECRET and JWT_SECRET |
| Trust client user_id | Always validate against token user_id |
| CORS allow_origins=["*"] | List specific allowed origins |
| Missing token expiration check | Use verify_exp=True in jwt.decode |
| Logging tokens | Never log JWT tokens or secrets |
| Token in URL | Use Authorization header only |

---

## 8. ERROR HANDLING

### Frontend Error States

```tsx
// components/auth/auth-error-boundary.tsx
'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'

interface AuthError {
  code: 'EXPIRED' | 'INVALID' | 'UNAUTHORIZED' | 'UNKNOWN'
  message: string
}

export function useAuthError() {
  const [error, setError] = useState<AuthError | null>(null)
  const router = useRouter()

  const handleAuthError = (err: Error) => {
    if (err.message.includes('expired')) {
      setError({ code: 'EXPIRED', message: 'Your session has expired' })
      router.push('/signin')
    } else if (err.message.includes('unauthorized') || err.message.includes('401')) {
      setError({ code: 'UNAUTHORIZED', message: 'Please sign in to continue' })
      router.push('/signin')
    } else {
      setError({ code: 'UNKNOWN', message: err.message })
    }
  }

  const clearError = () => setError(null)

  return { error, handleAuthError, clearError }
}
```

### Backend Error Responses

```python
# backend/auth.py - Enhanced error handling
from enum import Enum

class AuthErrorCode(str, Enum):
    EXPIRED = "TOKEN_EXPIRED"
    INVALID = "TOKEN_INVALID"
    MISSING = "TOKEN_MISSING"
    FORBIDDEN = "ACCESS_FORBIDDEN"


def create_auth_error(code: AuthErrorCode, message: str) -> HTTPException:
    """Create standardized auth error response"""
    status_map = {
        AuthErrorCode.EXPIRED: status.HTTP_401_UNAUTHORIZED,
        AuthErrorCode.INVALID: status.HTTP_401_UNAUTHORIZED,
        AuthErrorCode.MISSING: status.HTTP_401_UNAUTHORIZED,
        AuthErrorCode.FORBIDDEN: status.HTTP_403_FORBIDDEN,
    }

    return HTTPException(
        status_code=status_map[code],
        detail={"code": code.value, "message": message},
        headers={"WWW-Authenticate": "Bearer"}
    )
```

---

## 9. TESTING AUTHENTICATION

### Frontend Auth Tests

```typescript
// __tests__/auth.test.ts
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { SignInPage } from '@/app/(auth)/signin/page'

// Mock the auth client
jest.mock('@/lib/auth-client', () => ({
  signIn: {
    email: jest.fn(),
  },
}))

describe('SignIn Page', () => {
  it('shows error on invalid credentials', async () => {
    const { signIn } = require('@/lib/auth-client')
    signIn.email.mockResolvedValue({
      error: { message: 'Invalid credentials' }
    })

    render(<SignInPage />)

    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'test@example.com' },
    })
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'wrongpassword' },
    })
    fireEvent.click(screen.getByRole('button', { name: /sign in/i }))

    await waitFor(() => {
      expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument()
    })
  })
})
```

### Backend Auth Tests

```python
# backend/tests/test_auth.py
import pytest
import jwt
from fastapi.testclient import TestClient
from datetime import datetime, timedelta

from main import app
from config import settings


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def valid_token():
    """Generate a valid JWT token for testing"""
    payload = {
        "sub": "test-user-123",
        "email": "test@example.com",
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


@pytest.fixture
def expired_token():
    """Generate an expired JWT token"""
    payload = {
        "sub": "test-user-123",
        "exp": datetime.utcnow() - timedelta(hours=1)
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def test_protected_route_with_valid_token(client, valid_token):
    """Test that valid token allows access"""
    response = client.get(
        "/api/test-user-123/tasks",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 200


def test_protected_route_without_token(client):
    """Test that missing token returns 401"""
    response = client.get("/api/test-user-123/tasks")
    assert response.status_code == 401


def test_protected_route_with_expired_token(client, expired_token):
    """Test that expired token returns 401"""
    response = client.get(
        "/api/test-user-123/tasks",
        headers={"Authorization": f"Bearer {expired_token}"}
    )
    assert response.status_code == 401
    assert "expired" in response.json()["detail"].lower()


def test_user_cannot_access_other_users_data(client, valid_token):
    """Test that user cannot access another user's resources"""
    # Token is for test-user-123, but we're requesting other-user's data
    response = client.get(
        "/api/other-user-456/tasks",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 403
```

---

## 10. COMPLETE INTEGRATION EXAMPLE

### Full Authentication Flow

```typescript
// Example: Complete todo page with auth integration
// app/(dashboard)/todos/page.tsx

import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'
import { auth } from '@/lib/auth'
import { TodoListClient } from '@/components/todos/todo-list-client'

export default async function TodosPage() {
  // 1. Check for session cookie
  const cookieStore = await cookies()
  const sessionToken = cookieStore.get('better-auth.session_token')?.value

  if (!sessionToken) {
    redirect('/signin')
  }

  // 2. Validate session and get user data
  const session = await auth.api.getSession({
    headers: {
      cookie: `better-auth.session_token=${sessionToken}`,
    },
  })

  if (!session) {
    redirect('/signin')
  }

  // 3. Fetch user's todos from backend (server-side)
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/api/${session.user.id}/tasks`,
    {
      headers: {
        'Authorization': `Bearer ${session.session.token}`,
        'Content-Type': 'application/json',
      },
      next: { revalidate: 0 },
    }
  )

  if (!res.ok) {
    if (res.status === 401) {
      redirect('/signin')
    }
    throw new Error('Failed to fetch todos')
  }

  const todos = await res.json()

  // 4. Render with user context
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">
        Welcome, {session.user.name}
      </h1>
      <TodoListClient
        initialTodos={todos}
        userId={session.user.id}
      />
    </div>
  )
}
```

---

## Quick Reference

| Component | File | Purpose |
|-----------|------|---------|
| Auth Client | `lib/auth-client.ts` | Client-side auth methods |
| Auth Server | `lib/auth.ts` | Server-side auth config |
| Auth Route | `app/api/auth/[...all]/route.ts` | Better Auth handler |
| Signup Page | `app/(auth)/signup/page.tsx` | User registration |
| Signin Page | `app/(auth)/signin/page.tsx` | User login |
| JWT Verify | `backend/auth.py` | Token verification |

| Error | Status | Meaning |
|-------|--------|---------|
| Token missing | 401 | No Authorization header |
| Token invalid | 401 | Bad signature or format |
| Token expired | 401 | Past expiration time |
| Wrong user | 403 | Token user != path user |

---

## Execution

When this skill is invoked, Claude should:

1. **Analyze the request** to determine which auth pattern applies
2. **Verify secret synchronization** - BETTER_AUTH_SECRET = JWT_SECRET
3. **Implement frontend auth** with Better Auth client
4. **Implement backend verification** with PyJWT
5. **Add user authorization** checks on all endpoints
6. **Include proper error handling** for auth failures
7. **Test the full flow** - signup, signin, protected routes

### Example Prompts

- "Set up authentication for the app"
- "Create signup and signin pages"
- "Add JWT verification to the backend"
- "Implement protected routes"
- "Fix authentication not working between frontend and backend"
- "Add logout functionality"
