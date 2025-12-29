# UI Components Specification

## Component Library: Custom + Tailwind CSS

## Core Components

### 1. TaskList
**Purpose:** Display list of tasks with filtering
**Props:**
- `userId: string` - Current user ID
- `filter: 'all' | 'pending' | 'completed'`

**Features:**
- Shows all tasks or filtered by status
- Loading state while fetching
- Empty state when no tasks
- Click task to edit
- Delete button per task
- Complete/incomplete toggle

**Layout:**
```
┌─────────────────────────────────────┐
│ Filters: [All] [Pending] [Complete]│
├─────────────────────────────────────┤
│ ☐ Buy groceries          [Edit][Del]│
│   Milk, eggs, bread                 │
├─────────────────────────────────────┤
│ ☑ Call dentist           [Edit][Del]│
│   Schedule appointment              │
└─────────────────────────────────────┘
```

---

### 2. TaskItem
**Purpose:** Display individual task
**Props:**
- `task: Task` - Task object
- `onToggle: (id) => void`
- `onEdit: (id) => void`
- `onDelete: (id) => void`

**Features:**
- Checkbox for completion toggle
- Strikethrough for completed tasks
- Edit and delete buttons
- Truncated description (expand on click)

---

### 3. TaskForm
**Purpose:** Create or edit task
**Props:**
- `task?: Task` - Existing task (for edit mode)
- `onSubmit: (data) => void`
- `onCancel: () => void`

**Features:**
- Title input (required, max 200 chars)
- Description textarea (optional, max 1000 chars)
- Submit button (disabled while loading)
- Cancel button
- Client-side validation
- Error messages

**Layout:**
```
┌─────────────────────────────────┐
│ Title: [________________]       │
│                                 │
│ Description:                    │
│ [                          ]    │
│ [                          ]    │
│                                 │
│ [Cancel]         [Save Task]    │
└─────────────────────────────────┘
```

---

### 4. AuthGuard
**Purpose:** Protect routes requiring authentication
**Props:**
- `children: ReactNode`

**Features:**
- Checks if user is logged in
- Redirects to signin if not authenticated
- Shows loading spinner while checking
- Wraps dashboard and protected pages

---

### 5. Layout
**Purpose:** Common layout with header and navigation
**Props:**
- `children: ReactNode`

**Features:**
- Header with app name
- User email display
- Sign out button
- Main content area
- Responsive design

**Layout:**
```
┌─────────────────────────────────────┐
│ Todo App    user@email.com  [Logout]│
├─────────────────────────────────────┤
│                                     │
│          {children}                 │
│                                     │
└─────────────────────────────────────┘
```

---

### 6. Button
**Purpose:** Reusable button component
**Props:**
- `variant: 'primary' | 'secondary' | 'danger'`
- `disabled: boolean`
- `loading: boolean`
- `onClick: () => void`
- `children: ReactNode`

**Variants:**
- Primary: Blue background
- Secondary: Gray background
- Danger: Red background (for delete)

---

### 7. Input
**Purpose:** Reusable text input
**Props:**
- `type: 'text' | 'email' | 'password'`
- `value: string`
- `onChange: (value) => void`
- `placeholder: string`
- `error?: string`
- `required: boolean`

**Features:**
- Label
- Error message display
- Validation styling

---

### 8. Textarea
**Purpose:** Multi-line text input
**Props:**
- `value: string`
- `onChange: (value) => void`
- `placeholder: string`
- `rows: number`
- `maxLength: number`

---

## Color Scheme (Tailwind)
- Primary: `bg-blue-500`, `text-blue-500`
- Secondary: `bg-gray-500`, `text-gray-500`
- Success: `bg-green-500`, `text-green-500`
- Danger: `bg-red-500`, `text-red-500`
- Background: `bg-gray-50`
- Text: `text-gray-900`

## Responsive Breakpoints
- Mobile: default (< 640px)
- Tablet: `md:` (>= 768px)
- Desktop: `lg:` (>= 1024px)
