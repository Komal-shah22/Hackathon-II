# Feature: Task CRUD Operations

## User Stories

### US1: Create Task
**As a** logged-in user
**I want to** create a new task
**So that** I can track things I need to do

**Acceptance Criteria:**
- User can enter task title (required, 1-200 chars)
- User can enter task description (optional, max 1000 chars)
- Task is created with completed=false by default
- Task is associated with current user
- Success message shown after creation
- Task appears in task list immediately

### US2: View Tasks
**As a** logged-in user
**I want to** view all my tasks
**So that** I can see what I need to do

**Acceptance Criteria:**
- User sees only their own tasks
- Tasks displayed with title, description, status
- Tasks can be filtered by status (all/pending/completed)
- Empty state shown when no tasks
- Loading state shown while fetching

### US3: Update Task
**As a** logged-in user
**I want to** update a task's title or description
**So that** I can correct or clarify my tasks

**Acceptance Criteria:**
- User can edit task title
- User can edit task description
- Changes saved to database
- Updated task shown immediately
- User can only edit their own tasks

### US4: Delete Task
**As a** logged-in user
**I want to** delete a task
**So that** I can remove completed or unwanted tasks

**Acceptance Criteria:**
- User can delete any of their tasks
- Confirmation prompt shown before deletion
- Task removed from database
- Task removed from UI immediately
- User can only delete their own tasks

### US5: Mark Complete
**As a** logged-in user
**I want to** mark tasks as complete/incomplete
**So that** I can track my progress

**Acceptance Criteria:**
- User can toggle task completion status
- Status persists to database
- Visual indicator shows completed tasks (strikethrough, color)
- User can filter by completed/pending
- User can only toggle their own tasks

## Edge Cases
- Empty title → Show validation error
- Title too long (>200 chars) → Show validation error
- Network error → Show retry option
- Unauthorized access → Redirect to signin
- Task not found → Show error message
- Database error → Show generic error

## Technical Requirements
- All operations secured with JWT
- User ID validation on every request
- Optimistic UI updates
- Error handling and user feedback
- Loading states for all async operations
