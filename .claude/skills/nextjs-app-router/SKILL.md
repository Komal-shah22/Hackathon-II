---
description: Next.js 16 App Router patterns, server/client components, and best practices. Use when building Next.js frontend, creating pages, or when user mentions Next.js, frontend, or React components.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Skill: Next.js 16 App Router Patterns

This skill teaches Claude the Next.js 16 App Router patterns, server/client component best practices, and modern React patterns for building the todo application frontend.

---

## 1. PROJECT STRUCTURE

### Standard App Router Structure

```
app/
├── layout.tsx              # Root layout (Server Component)
├── page.tsx                # Homepage (Server Component)
├── loading.tsx             # Root loading UI
├── error.tsx               # Root error boundary (Client Component)
├── not-found.tsx           # 404 page
├── globals.css             # Global styles
│
├── (auth)/                 # Route group for auth pages (no URL impact)
│   ├── login/
│   │   └── page.tsx
│   ├── signup/
│   │   └── page.tsx
│   └── layout.tsx          # Shared auth layout
│
├── (dashboard)/            # Route group for authenticated pages
│   ├── layout.tsx          # Dashboard layout with nav
│   ├── todos/
│   │   ├── page.tsx        # Todo list
│   │   ├── loading.tsx     # Todo-specific loading
│   │   ├── [id]/
│   │   │   └── page.tsx    # Single todo view
│   │   └── new/
│   │       └── page.tsx    # Create todo form
│   └── settings/
│       └── page.tsx
│
├── api/                    # API routes (if needed for BFF pattern)
│   └── [...nextauth]/
│       └── route.ts
│
components/
├── ui/                     # Reusable UI primitives
│   ├── button.tsx
│   ├── input.tsx
│   ├── card.tsx
│   └── modal.tsx
├── forms/                  # Form components
│   └── todo-form.tsx
├── todos/                  # Feature-specific components
│   ├── todo-card.tsx
│   ├── todo-list.tsx
│   └── todo-filter.tsx
└── layout/                 # Layout components
    ├── header.tsx
    ├── sidebar.tsx
    └── nav.tsx

lib/
├── api.ts                  # API client for backend calls
├── auth.ts                 # Auth configuration (Better Auth)
├── utils.ts                # Utility functions
└── hooks/                  # Custom React hooks
    ├── use-todos.ts
    └── use-auth.ts

types/
├── todo.ts                 # Todo-related types
└── api.ts                  # API response types
```

### Key Conventions

- **Route Groups**: `(groupName)` folders organize routes without affecting URL
- **Dynamic Routes**: `[param]` for single param, `[...slug]` for catch-all
- **Private Folders**: `_folderName` excluded from routing
- **Parallel Routes**: `@slotName` for multiple pages in same layout
- **Intercepting Routes**: `(.)`, `(..)`, `(...)` for modal patterns

---

## 2. SERVER VS CLIENT COMPONENTS

### Decision Framework

```
┌─────────────────────────────────────────────────────────────┐
│                    COMPONENT DECISION TREE                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Does it need browser APIs (window, localStorage)?           │
│     YES → Client Component                                   │
│     NO  ↓                                                    │
│                                                              │
│  Does it need event handlers (onClick, onChange)?            │
│     YES → Client Component                                   │
│     NO  ↓                                                    │
│                                                              │
│  Does it use React hooks (useState, useEffect)?              │
│     YES → Client Component                                   │
│     NO  ↓                                                    │
│                                                              │
│  Does it need real-time updates or user interaction?         │
│     YES → Client Component                                   │
│     NO  → Server Component (default)                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Server Components (Default)

```tsx
// app/todos/page.tsx - Server Component (no 'use client')
import { getTodos } from '@/lib/api'
import { TodoList } from '@/components/todos/todo-list'

export default async function TodosPage() {
  // Direct data fetching - runs on server
  const todos = await getTodos()

  return (
    <main className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">My Todos</h1>
      <TodoList todos={todos} />
    </main>
  )
}
```

**Server Component Benefits:**
- Zero JavaScript sent to client for component logic
- Direct database/API access without client exposure
- Automatic code splitting
- Better SEO and initial page load

### Client Components

```tsx
// components/todos/todo-card.tsx
'use client'

import { useState } from 'react'
import { Todo } from '@/types/todo'
import { updateTodo, deleteTodo } from '@/lib/api'

interface TodoCardProps {
  todo: Todo
  onUpdate: () => void
}

export function TodoCard({ todo, onUpdate }: TodoCardProps) {
  const [isEditing, setIsEditing] = useState(false)
  const [isLoading, setIsLoading] = useState(false)

  const handleToggle = async () => {
    setIsLoading(true)
    await updateTodo(todo.id, { completed: !todo.completed })
    onUpdate()
    setIsLoading(false)
  }

  const handleDelete = async () => {
    setIsLoading(true)
    await deleteTodo(todo.id)
    onUpdate()
  }

  return (
    <div className="p-4 border rounded-lg flex items-center gap-4">
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={handleToggle}
        disabled={isLoading}
        className="h-5 w-5"
      />
      <span className={todo.completed ? 'line-through text-gray-500' : ''}>
        {todo.title}
      </span>
      <button
        onClick={handleDelete}
        disabled={isLoading}
        className="ml-auto text-red-500 hover:text-red-700"
      >
        Delete
      </button>
    </div>
  )
}
```

### Composition Pattern: Server → Client

```tsx
// app/todos/page.tsx (Server Component)
import { getTodos } from '@/lib/api'
import { TodoListClient } from '@/components/todos/todo-list-client'

export default async function TodosPage() {
  const initialTodos = await getTodos()

  // Pass server-fetched data to client component
  return <TodoListClient initialTodos={initialTodos} />
}

// components/todos/todo-list-client.tsx (Client Component)
'use client'

import { useState } from 'react'
import { Todo } from '@/types/todo'
import { TodoCard } from './todo-card'

export function TodoListClient({ initialTodos }: { initialTodos: Todo[] }) {
  const [todos, setTodos] = useState(initialTodos)

  const refreshTodos = async () => {
    const res = await fetch('/api/todos')
    const data = await res.json()
    setTodos(data)
  }

  return (
    <div className="space-y-2">
      {todos.map(todo => (
        <TodoCard key={todo.id} todo={todo} onUpdate={refreshTodos} />
      ))}
    </div>
  )
}
```

---

## 3. DATA FETCHING PATTERNS

### Server-Side Fetching (Recommended)

```tsx
// lib/api.ts
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export async function getTodos(token?: string): Promise<Todo[]> {
  const res = await fetch(`${API_URL}/api/tasks`, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    // Next.js 15+ caching options
    next: {
      revalidate: 60, // Revalidate every 60 seconds
      tags: ['todos'] // For on-demand revalidation
    }
  })

  if (!res.ok) throw new Error('Failed to fetch todos')
  return res.json()
}

// For mutations
export async function createTodo(data: CreateTodoInput, token: string): Promise<Todo> {
  const res = await fetch(`${API_URL}/api/tasks`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })

  if (!res.ok) throw new Error('Failed to create todo')
  return res.json()
}
```

### With Authentication

```tsx
// app/todos/page.tsx
import { cookies } from 'next/headers'
import { getTodos } from '@/lib/api'
import { redirect } from 'next/navigation'

export default async function TodosPage() {
  const cookieStore = await cookies()
  const token = cookieStore.get('session')?.value

  if (!token) {
    redirect('/login')
  }

  const todos = await getTodos(token)

  return <TodoList todos={todos} />
}
```

### Client-Side Fetching with SWR

```tsx
// hooks/use-todos.ts
'use client'

import useSWR from 'swr'
import { Todo } from '@/types/todo'

const fetcher = (url: string) => fetch(url).then(res => res.json())

export function useTodos() {
  const { data, error, isLoading, mutate } = useSWR<Todo[]>(
    '/api/todos',
    fetcher,
    {
      revalidateOnFocus: true,
      revalidateOnReconnect: true,
    }
  )

  return {
    todos: data ?? [],
    isLoading,
    isError: error,
    refresh: mutate,
  }
}
```

---

## 4. LAYOUTS AND TEMPLATES

### Root Layout (Required)

```tsx
// app/layout.tsx
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Providers } from '@/components/providers'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Todo App',
  description: 'A modern todo application',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  )
}
```

### Nested Layout with Navigation

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
  const session = cookieStore.get('session')

  if (!session) {
    redirect('/login')
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

### Template (Re-renders on Navigation)

```tsx
// app/(dashboard)/template.tsx
'use client'

import { motion } from 'framer-motion'

export default function Template({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      {children}
    </motion.div>
  )
}
```

---

## 5. LOADING AND ERROR STATES

### Loading UI (loading.tsx)

```tsx
// app/todos/loading.tsx
export default function Loading() {
  return (
    <div className="space-y-4">
      {[...Array(5)].map((_, i) => (
        <div key={i} className="animate-pulse">
          <div className="h-16 bg-gray-200 rounded-lg" />
        </div>
      ))}
    </div>
  )
}
```

### Streaming with Suspense

```tsx
// app/todos/page.tsx
import { Suspense } from 'react'
import { TodoList } from '@/components/todos/todo-list'
import { TodoStats } from '@/components/todos/todo-stats'

export default function TodosPage() {
  return (
    <div className="space-y-6">
      <h1>My Todos</h1>

      {/* Stats load independently */}
      <Suspense fallback={<StatsSkeletion />}>
        <TodoStats />
      </Suspense>

      {/* List loads independently */}
      <Suspense fallback={<ListSkeleton />}>
        <TodoList />
      </Suspense>
    </div>
  )
}
```

### Error Boundary

```tsx
// app/todos/error.tsx
'use client'

import { useEffect } from 'react'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    // Log error to monitoring service
    console.error(error)
  }, [error])

  return (
    <div className="flex flex-col items-center justify-center min-h-[400px]">
      <h2 className="text-xl font-semibold text-red-600">
        Something went wrong!
      </h2>
      <p className="text-gray-600 mt-2">{error.message}</p>
      <button
        onClick={reset}
        className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Try again
      </button>
    </div>
  )
}
```

### Global Error Handler

```tsx
// app/global-error.tsx
'use client'

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <html>
      <body>
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <h1 className="text-2xl font-bold text-red-600">
              Application Error
            </h1>
            <button onClick={reset} className="mt-4 btn-primary">
              Restart Application
            </button>
          </div>
        </div>
      </body>
    </html>
  )
}
```

---

## 6. FORMS AND SERVER ACTIONS

### Server Actions (Next.js 15+)

```tsx
// app/todos/actions.ts
'use server'

import { revalidatePath, revalidateTag } from 'next/cache'
import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'

export async function createTodo(formData: FormData) {
  const cookieStore = await cookies()
  const token = cookieStore.get('session')?.value

  if (!token) {
    redirect('/login')
  }

  const title = formData.get('title') as string
  const description = formData.get('description') as string

  const res = await fetch(`${process.env.API_URL}/api/tasks`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ title, description }),
  })

  if (!res.ok) {
    throw new Error('Failed to create todo')
  }

  revalidateTag('todos')
  revalidatePath('/todos')
}

export async function toggleTodo(id: string, completed: boolean) {
  const cookieStore = await cookies()
  const token = cookieStore.get('session')?.value

  await fetch(`${process.env.API_URL}/api/tasks/${id}`, {
    method: 'PATCH',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ completed }),
  })

  revalidateTag('todos')
}

export async function deleteTodo(id: string) {
  const cookieStore = await cookies()
  const token = cookieStore.get('session')?.value

  await fetch(`${process.env.API_URL}/api/tasks/${id}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  })

  revalidateTag('todos')
  revalidatePath('/todos')
}
```

### Form with Server Action

```tsx
// components/forms/todo-form.tsx
'use client'

import { useFormStatus } from 'react-dom'
import { createTodo } from '@/app/todos/actions'

function SubmitButton() {
  const { pending } = useFormStatus()

  return (
    <button
      type="submit"
      disabled={pending}
      className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50"
    >
      {pending ? 'Creating...' : 'Create Todo'}
    </button>
  )
}

export function TodoForm() {
  return (
    <form action={createTodo} className="space-y-4">
      <div>
        <label htmlFor="title" className="block text-sm font-medium">
          Title
        </label>
        <input
          type="text"
          id="title"
          name="title"
          required
          className="mt-1 w-full px-3 py-2 border rounded-md"
        />
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium">
          Description
        </label>
        <textarea
          id="description"
          name="description"
          rows={3}
          className="mt-1 w-full px-3 py-2 border rounded-md"
        />
      </div>

      <SubmitButton />
    </form>
  )
}
```

### Form with Validation (useActionState)

```tsx
// components/forms/todo-form-validated.tsx
'use client'

import { useActionState } from 'react'
import { createTodoWithValidation } from '@/app/todos/actions'

type FormState = {
  errors?: {
    title?: string[]
    description?: string[]
  }
  message?: string
}

export function TodoFormValidated() {
  const [state, formAction, isPending] = useActionState<FormState, FormData>(
    createTodoWithValidation,
    {}
  )

  return (
    <form action={formAction} className="space-y-4">
      <div>
        <label htmlFor="title">Title</label>
        <input
          type="text"
          id="title"
          name="title"
          className="w-full border rounded px-3 py-2"
        />
        {state.errors?.title && (
          <p className="text-red-500 text-sm">{state.errors.title[0]}</p>
        )}
      </div>

      <button
        type="submit"
        disabled={isPending}
        className="btn-primary"
      >
        {isPending ? 'Creating...' : 'Create'}
      </button>

      {state.message && (
        <p className="text-green-600">{state.message}</p>
      )}
    </form>
  )
}
```

---

## 7. AUTHENTICATION INTEGRATION

### Auth Context Provider

```tsx
// components/providers/auth-provider.tsx
'use client'

import { createContext, useContext, ReactNode } from 'react'
import { createAuthClient } from 'better-auth/react'

const authClient = createAuthClient()

const AuthContext = createContext<typeof authClient | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  return (
    <AuthContext.Provider value={authClient}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
```

### Protected Route Wrapper

```tsx
// components/auth/protected-route.tsx
import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'

export async function ProtectedRoute({
  children,
}: {
  children: React.ReactNode
}) {
  const cookieStore = await cookies()
  const session = cookieStore.get('session')

  if (!session) {
    redirect('/login')
  }

  return <>{children}</>
}
```

### Login Page

```tsx
// app/(auth)/login/page.tsx
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/components/providers/auth-provider'
import Link from 'next/link'

export default function LoginPage() {
  const router = useRouter()
  const auth = useAuth()
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')

    const formData = new FormData(e.currentTarget)
    const email = formData.get('email') as string
    const password = formData.get('password') as string

    try {
      await auth.signIn.email({
        email,
        password,
      })
      router.push('/todos')
      router.refresh()
    } catch (err) {
      setError('Invalid email or password')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="w-full max-w-md p-8 space-y-6 bg-white rounded-lg shadow">
        <h1 className="text-2xl font-bold text-center">Sign In</h1>

        {error && (
          <div className="p-3 bg-red-100 text-red-700 rounded">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              required
              className="w-full px-3 py-2 border rounded"
            />
          </div>

          <div>
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              required
              className="w-full px-3 py-2 border rounded"
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
          >
            {isLoading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <p className="text-center text-gray-600">
          Don't have an account?{' '}
          <Link href="/signup" className="text-blue-600 hover:underline">
            Sign up
          </Link>
        </p>
      </div>
    </div>
  )
}
```

---

## 8. API CLIENT PATTERN

### Typed API Client

```tsx
// lib/api-client.ts
import { Todo, CreateTodoInput, UpdateTodoInput } from '@/types/todo'

class ApiClient {
  private baseUrl: string

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  }

  private async getToken(): Promise<string | null> {
    // Client-side: get from cookie or auth state
    if (typeof window !== 'undefined') {
      const cookies = document.cookie.split(';')
      const sessionCookie = cookies.find(c => c.trim().startsWith('session='))
      return sessionCookie?.split('=')[1] || null
    }
    return null
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = await this.getToken()

    const res = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
        ...options.headers,
      },
    })

    if (!res.ok) {
      const error = await res.json().catch(() => ({}))
      throw new Error(error.detail || 'API request failed')
    }

    return res.json()
  }

  // Todos
  async getTodos(): Promise<Todo[]> {
    return this.request<Todo[]>('/api/tasks')
  }

  async getTodo(id: string): Promise<Todo> {
    return this.request<Todo>(`/api/tasks/${id}`)
  }

  async createTodo(data: CreateTodoInput): Promise<Todo> {
    return this.request<Todo>('/api/tasks', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  async updateTodo(id: string, data: UpdateTodoInput): Promise<Todo> {
    return this.request<Todo>(`/api/tasks/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    })
  }

  async deleteTodo(id: string): Promise<void> {
    return this.request<void>(`/api/tasks/${id}`, {
      method: 'DELETE',
    })
  }
}

export const api = new ApiClient()
```

### Types

```tsx
// types/todo.ts
export interface Todo {
  id: string
  title: string
  description?: string
  completed: boolean
  created_at: string
  updated_at: string
  user_id: string
}

export interface CreateTodoInput {
  title: string
  description?: string
}

export interface UpdateTodoInput {
  title?: string
  description?: string
  completed?: boolean
}
```

---

## 9. BEST PRACTICES CHECKLIST

### Component Guidelines

- [ ] Default to Server Components
- [ ] Add 'use client' only when needed (hooks, events, browser APIs)
- [ ] Keep client components small and focused
- [ ] Use composition: Server components pass data to Client components

### Data Fetching

- [ ] Fetch data in Server Components when possible
- [ ] Use `next: { revalidate }` for caching strategies
- [ ] Implement proper error handling with error.tsx
- [ ] Use Suspense for streaming content

### Forms

- [ ] Use Server Actions for form submissions
- [ ] Implement useFormStatus for loading states
- [ ] Add proper validation with error feedback
- [ ] Use useActionState for complex form state

### Performance

- [ ] Minimize 'use client' boundaries
- [ ] Use dynamic imports for heavy client components
- [ ] Implement proper loading states
- [ ] Use Next.js Image for optimized images

### Security

- [ ] Validate all user input server-side
- [ ] Never expose sensitive data in client components
- [ ] Use environment variables for secrets
- [ ] Implement CSRF protection for forms

---

## 10. COMMON PATTERNS

### Optimistic Updates

```tsx
'use client'

import { useOptimistic, useTransition } from 'react'
import { toggleTodoAction } from '@/app/todos/actions'

export function TodoItem({ todo }: { todo: Todo }) {
  const [isPending, startTransition] = useTransition()
  const [optimisticTodo, setOptimisticTodo] = useOptimistic(
    todo,
    (state, completed: boolean) => ({ ...state, completed })
  )

  const handleToggle = () => {
    startTransition(async () => {
      setOptimisticTodo(!optimisticTodo.completed)
      await toggleTodoAction(todo.id, !todo.completed)
    })
  }

  return (
    <div className={isPending ? 'opacity-50' : ''}>
      <input
        type="checkbox"
        checked={optimisticTodo.completed}
        onChange={handleToggle}
      />
      <span>{todo.title}</span>
    </div>
  )
}
```

### Modal with Parallel Routes

```tsx
// app/@modal/(.)todos/[id]/page.tsx
import { Modal } from '@/components/ui/modal'
import { getTodo } from '@/lib/api'

export default async function TodoModal({
  params,
}: {
  params: { id: string }
}) {
  const todo = await getTodo(params.id)

  return (
    <Modal>
      <h2>{todo.title}</h2>
      <p>{todo.description}</p>
    </Modal>
  )
}

// app/layout.tsx
export default function Layout({
  children,
  modal,
}: {
  children: React.ReactNode
  modal: React.ReactNode
}) {
  return (
    <>
      {children}
      {modal}
    </>
  )
}
```

---

## Quick Reference

| Pattern | When to Use |
|---------|-------------|
| Server Component | Default, data fetching, no interactivity |
| Client Component | Hooks, events, browser APIs |
| Server Action | Form submissions, mutations |
| loading.tsx | Page-level loading states |
| error.tsx | Page-level error handling |
| Suspense | Component-level streaming |
| Route Groups | Organize routes without URL impact |
| Parallel Routes | Multiple pages in same layout (modals) |

---

## Execution

When this skill is invoked, Claude should:

1. **Analyze the request** to determine which App Router pattern applies
2. **Check existing code** for patterns and consistency
3. **Generate code** following the patterns above
4. **Prefer Server Components** unless client interactivity is required
5. **Include proper TypeScript types** for all components
6. **Add loading and error states** where appropriate
7. **Follow the project structure** conventions

### Example Prompts

- "Create a new todo page with server-side data fetching"
- "Build a todo form with server actions and validation"
- "Set up the dashboard layout with sidebar navigation"
- "Add optimistic updates to the todo toggle"
- "Implement protected routes for authenticated pages"
