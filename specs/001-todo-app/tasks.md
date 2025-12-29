# Tasks: Phase 2 Full-Stack Todo Application

**Input**: Design documents from `/specs/001-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required), contracts/openapi.yaml
**Tests**: Not explicitly requested - tests can be added per agent workflow

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for both frontend and backend

### 1.1 Frontend Setup

- [x] T001 Initialize Next.js 16 project with TypeScript in frontend/
- [x] T002 Configure TypeScript strict mode in frontend/tsconfig.json
- [x] T003 [P] Setup Tailwind CSS in frontend/tailwind.config.ts
- [x] T004 [P] Install and initialize Shadcn UI in frontend/components/ui/
- [x] T005 [P] Create folder structure in frontend/app/, frontend/components/, frontend/lib/
- [x] T006 Create .env.example for frontend environment variables

### 1.2 Backend Setup

- [x] T007 Create backend/ directory with FastAPI structure
- [x] T008 [P] Create requirements.txt with FastAPI, SQLModel, Pydantic, python-jose, passlib
- [x] T009 [P] Create .env.example for backend environment variables
- [x] T010 [P] Create main.py entry point in backend/
- [x] T011 [P] Configure CORS and middleware in backend/main.py

### 1.3 Development Tools

- [x] T012 [P] Setup ESLint and Prettier for frontend
- [x] T013 [P] Setup pytest and coverage for backend
- [x] T014 [P] Create docker-compose.yml for local development (optional)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can implement

**CRITICAL**: No user story work can begin until this phase is complete

### 2.1 Database Foundation

- [x] T015 Create db.py with SQLModel connection to Neon PostgreSQL in backend/db.py
- [x] T016 [P] Create Task SQLModel with ALL fields (basic + intermediate + advanced) in backend/models.py
- [x] T017 [P] Create SQLModel enums (TaskPriority, TaskCategory, RecurrencePattern) in backend/models.py
- [x] T018 [P] Create database indexes for user_id, priority, category, due_date, completed in backend/models.py
- [x] T019 Create create_tables() function in backend/db.py

### 2.2 Authentication Foundation

- [x] T020 Create JWT verification middleware in backend/auth.py
- [x] T021 [P] Create get_current_user dependency in backend/auth.py
- [x] T022 [P] Create password hashing utilities in backend/auth.py
- [x] T023 Create Pydantic schemas for authentication in backend/schemas.py

### 2.3 API Foundation

- [x] T024 Create API router structure in backend/routes/__init__.py
- [x] T025 [P] Create task Pydantic schemas (TaskCreate, TaskUpdate, TaskResponse) in backend/schemas.py
- [x] T026 [P] Create error handling utilities in backend/main.py

### 2.4 Frontend Foundation

- [x] T027 Create API client with JWT handling in frontend/lib/api.ts
- [x] T028 [P] Create TypeScript types for Task, User, API responses in frontend/lib/types.ts
- [x] T029 [P] Create auth context and provider in frontend/components/auth/AuthProvider.tsx
- [x] T030 [P] Create utility functions in frontend/lib/utils.ts

### 2.5 Layout Foundation

- [x] T031 Create root layout in frontend/app/layout.tsx
- [x] T032 [P] Create auth layout group in frontend/app/(auth)/layout.tsx
- [x] T033 [P] Create dashboard layout group in frontend/app/(dashboard)/layout.tsx

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Authentication (Priority: P1) MVP

**Goal**: Users can create accounts, login, logout, and access protected pages

**Independent Test**: Create an account, verify email format, confirm after login only user's own tasks are visible

### Backend Implementation

- [x] T034 [US1] Create signup endpoint POST /auth/signup in backend/routes/auth.py
- [x] T035 [US1] Create signin endpoint POST /auth/signin in backend/routes/auth.py
- [x] T036 [US1] Create GET /auth/me endpoint in backend/routes/auth.py
- [x] T037 [US1] Create POST /auth/logout endpoint in backend/routes/auth.py
- [x] T038 [US1] Add JWT token generation on signup/signin in backend/routes/auth.py
- [x] T039 [US1] Add email validation and password strength requirements in backend/schemas.py

### Frontend Implementation

- [x] T040 [US1] Create signup page in frontend/app/(auth)/signup/page.tsx
- [x] T041 [US1] Create signin page in frontend/app/(auth)/signin/page.tsx
- [x] T042 [US1] Create auth forms with validation in frontend/components/auth/
- [x] T043 [US1] Implement auth context with login/logout state in frontend/components/auth/AuthProvider.tsx
- [x] T044 [US1] Add auth redirect on protected route access in frontend/lib/api.ts
- [x] T045 [US1] Create loading and error states for auth operations in frontend/components/auth/

**Checkpoint**: User Story 1 complete - authentication system working

---

## Phase 4: User Story 2 - Basic Task Management (Priority: P1) MVP

**Goal**: Users can create, view, update, delete tasks and toggle completion

**Independent Test**: Perform all CRUD operations on tasks and verify persistence

### Backend Implementation

- [x] T046 [US2] Create GET /tasks endpoint with user isolation in backend/routes/tasks.py
- [x] T047 [US2] Create POST /tasks endpoint in backend/routes/tasks.py
- [x] T048 [US2] Create GET /tasks/{task_id} endpoint in backend/routes/tasks.py
- [x] T049 [US2] Create PUT /tasks/{task_id} endpoint in backend/routes/tasks.py
- [x] T050 [US2] Create DELETE /tasks/{task_id} endpoint in backend/routes/tasks.py
- [x] T051 [US2] Create PUT /tasks/{task_id}/complete endpoint in backend/routes/tasks.py
- [x] T052 [US2] Add user_id validation (token user_id must match resource user_id) in backend/routes/tasks.py

### Frontend Implementation

- [x] T053 [US2] Create TaskForm component in frontend/components/tasks/TaskForm.tsx
- [x] T054 [US2] Create TaskItem component in frontend/components/tasks/TaskItem.tsx
- [x] T055 [US2] Create TaskList component in frontend/components/tasks/TaskList.tsx
- [x] T056 [US2] Create dashboard page in frontend/app/(dashboard)/page.tsx
- [x] T057 [US2] Create useTasks hook in frontend/lib/hooks/useTasks.ts
- [x] T058 [US2] Implement optimistic updates for task operations in frontend/lib/hooks/useTasks.ts
- [x] T059 [US2] Add loading skeletons for task list in frontend/components/tasks/TaskList.tsx

**Checkpoint**: User Story 2 complete - basic task management working

---

## Phase 5: User Story 3 - Task Organization (Priority: P2)

**Goal**: Users can assign priorities and categories to tasks with visual indicators

**Independent Test**: Create tasks with different priorities and categories, verify assignments persist and display correctly

### Backend Implementation

- [x] T060 [US3] Update Task model with priority field in backend/models.py
- [x] T061 [US3] Update Task model with category field in backend/models.py
- [x] T062 [US3] Update Pydantic schemas to include priority and category in backend/schemas.py
- [x] T063 [US3] Add priority and category to task responses in backend/routes/tasks.py

### Frontend Implementation

- [x] T064 [US3] Add priority selector UI in TaskForm.tsx
- [x] T065 [US3] Add category selector UI in TaskForm.tsx
- [x] T066 [US3] Create priority badge component in frontend/components/tasks/TaskItem.tsx
- [x] T067 [US3] Create category tag component in frontend/components/tasks/TaskItem.tsx
- [x] T068 [US3] Display priority badges on TaskItem in frontend/components/tasks/TaskItem.tsx
- [x] T069 [US3] Display category tags on TaskItem in frontend/components/tasks/TaskItem.tsx
- [x] T070 [US3] Update TaskForm to include priority and category editing in frontend/components/tasks/TaskForm.tsx

**Checkpoint**: User Story 3 complete - priority and category system working

---

## Phase 6: User Story 4 - Search, Filter, and Sort (Priority: P2)

**Goal**: Users can find, narrow down, and reorder tasks efficiently

**Independent Test**: Create 20+ tasks with varied properties, verify search/filters/sorting work correctly

### Backend Implementation

- [x] T071 [US4] Add search query parameter to GET /tasks in backend/routes/tasks.py
- [x] T072 [US4] Add status filter (all/pending/completed) to GET /tasks in backend/routes/tasks.py
- [x] T073 [US4] Add priority filter to GET /tasks in backend/routes/tasks.py
- [x] T074 [US4] Add category filter to GET /tasks in backend/routes/tasks.py
- [x] T075 [US4] Add sort_by and sort_order parameters to GET /tasks in backend/routes/tasks.py

### Frontend Implementation

- [x] T076 [US4] Create TaskFilter component in frontend/components/tasks/TaskList.tsx
- [x] T077 [US4] Create search input component in frontend/components/tasks/TaskList.tsx
- [x] T078 [US4] Create sort selector component in frontend/components/tasks/TaskList.tsx
- [x] T079 [US4] Implement search (title/description) in frontend/components/tasks/TaskList.tsx
- [x] T080 [US4] Implement filter by status in frontend/components/tasks/TaskList.tsx
- [x] T081 [US4] Implement filter by priority in frontend/components/tasks/TaskList.tsx
- [x] T082 [US4] Implement filter by category in frontend/components/tasks/TaskList.tsx
- [x] T083 [US4] Implement sort functionality in frontend/components/tasks/TaskList.tsx
- [x] T084 [US4] Add clear filters button in frontend/components/tasks/TaskList.tsx
- [x] T085 [US4] Show active filter badges in frontend/components/tasks/TaskList.tsx

**Checkpoint**: User Story 4 complete - search, filter, and sort working

---

## Phase 7: User Story 5 - Due Dates and Reminders (Priority: P3)

**Goal**: Users can set deadlines and receive notifications before due dates

**Independent Test**: Set due dates on tasks and verify reminders trigger at specified time

### Backend Implementation

- [x] T086 [US5] Update Task model with due_date field in backend/models.py
- [x] T087 [US5] Update Task model with reminder_time field in backend/models.py
- [x] T088 [US5] Update Task model with reminder_sent field in backend/models.py
- [x] T089 [US5] Update Pydantic schemas for due_date and reminder_time in backend/schemas.py
- [x] T090 [US5] Add overdue task detection in backend/routes/tasks.py
- [x] T091 [US5] Create endpoint to mark reminder as sent in backend/routes/tasks.py

### Frontend Implementation

- [x] T092 [US5] Add date picker component for due_date in TaskForm.tsx
- [x] T093 [US5] Add time picker for due_date in TaskForm.tsx (optional)
- [x] T094 [US5] Add reminder time selector in TaskForm.tsx
- [x] T095 [US5] Create Browser Notification API service in frontend/lib/notifications.ts
- [x] T096 [US5] Request notification permission on user interaction in frontend/components/
- [x] T097 [US5] Implement reminder polling (every 60 seconds) in frontend/components/tasks/TaskList.tsx
- [x] T098 [US5] Display overdue highlighting in TaskItem.tsx
- [x] T099 [US5] Display "due today" indicator in TaskItem.tsx
- [x] T100 [US5] Show upcoming badge for tasks due soon in TaskItem.tsx

**Checkpoint**: User Story 5 complete - due dates and reminders working

---

## Phase 8: User Story 6 - Recurring Tasks (Priority: P3)

**Goal**: Tasks automatically recreate when marked complete based on recurrence pattern

**Independent Test**: Create recurring task, mark complete, verify new instance created

### Backend Implementation

- [x] T101 [US6] Update Task model with is_recurring field in backend/models.py
- [x] T102 [US6] Update Task model with recurrence_pattern field in backend/models.py
- [x] T103 [US6] Update Task model with recurrence_interval field in backend/models.py
- [x] T104 [US6] Update Task model with recurrence_days field in backend/models.py
- [x] T105 [US6] Update Task model with recurrence_end_date field in backend/models.py
- [x] T106 [US6] Update Task model with parent_task_id field in backend/models.py
- [x] T107 [US6] Create create_next_occurrence() function in backend/routes/tasks.py
- [x] T108 [US6] Update complete endpoint to create next occurrence in backend/routes/tasks.py

### Frontend Implementation

- [x] T109 [US6] Add recurrence selector UI in TaskForm.tsx
- [x] T110 [US6] Add recurrence interval and days UI in TaskForm.tsx
- [x] T111 [US6] Add recurrence end date picker in TaskForm.tsx
- [x] T112 [US6] Display recurring indicator on TaskItem in frontend/components/tasks/TaskItem.tsx
- [x] T113 [US6] Handle next occurrence display in TaskItem.tsx
- [x] T114 [US6] Add recurrence editing options in TaskForm.tsx

**Checkpoint**: User Story 6 complete - recurring tasks working

---

## Phase 9: User Story 7 - Task Statistics (Priority: P3)

**Goal**: Users can view productivity analytics and task breakdowns

**Independent Test**: Create and complete tasks, verify statistics reflect activity data accurately

### Backend Implementation

- [x] T115 [US7] Create GET /users/{user_id}/stats endpoint in backend/routes/tasks.py
- [x] T116 [US7] Implement database aggregation for total tasks in backend/routes/tasks.py
- [x] T117 [US7] Implement database aggregation for completed tasks in backend/routes/tasks.py
- [x] T118 [US7] Implement database aggregation for completion rate in backend/routes/tasks.py
- [x] T119 [US7] Implement database aggregation for overdue count in backend/routes/tasks.py
- [x] T120 [US7] Implement database aggregation for due today count in backend/routes/tasks.py
- [x] T121 [US7] Implement database aggregation by category in backend/routes/tasks.py
- [x] T122 [US7] Implement database aggregation by priority in backend/routes/tasks.py

### Frontend Implementation

- [x] T123 [US7] Create TaskStats component in frontend/components/tasks/TaskStats.tsx
- [x] T124 [US7] Create stats display cards (total, completed, rate) in frontend/components/tasks/TaskStats.tsx
- [x] T125 [US7] Create category breakdown chart in frontend/components/tasks/TaskStats.tsx
- [x] T126 [US7] Create priority breakdown chart in frontend/components/tasks/TaskStats.tsx
- [x] T127 [US7] Add stats view to dashboard in frontend/app/(dashboard)/page.tsx
- [x] T128 [US7] Add useStats hook in frontend/lib/hooks/useStats.ts

**Checkpoint**: User Story 7 complete - statistics dashboard working

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

### UI/UX Polish

- [x] T129 [P] Add animations and transitions with Framer Motion (optional) in frontend/
- [x] T130 [P] Improve empty states with illustrations in frontend/components/tasks/
- [x] T131 [P] Add toast notifications for user feedback in frontend/
- [x] T132 [P] Implement loading skeletons instead of spinners in frontend/components/

### Performance

- [x] T133 [P] Add pagination if task list exceeds 100 tasks in backend/routes/tasks.py
- [x] T134 [P] Optimize database queries with proper indexes in backend/models.py
- [x] T135 [P] Implement debouncing for search input in frontend/lib/hooks/useTasks.ts

### Accessibility

- [x] T136 [P] Add ARIA labels to all interactive elements in frontend/components/
- [x] T137 [P] Ensure keyboard navigation works in frontend/components/
- [x] T138 [P] Add focus indicators in frontend/components/

### Error Handling

- [x] T139 [P] Improve error messages for user-friendly display in frontend/
- [x] T140 [P] Add retry mechanism for network failures in frontend/lib/api.ts

### Documentation

- [x] T141 [P] Update README.md with feature overview
- [x] T142 [P] Add API documentation endpoint in backend/main.py

---

## Dependencies & Execution Order

### Phase Dependencies

| Phase | Depends On | Blocks |
|-------|------------|--------|
| Phase 1: Setup | None | Phase 2 |
| Phase 2: Foundational | Phase 1 | All User Stories |
| Phase 3: US1 Auth | Phase 2 | US2+ |
| Phase 4: US2 CRUD | Phase 2 | US3+ |
| Phase 5: US3 Org | Phase 2 | US4+ |
| Phase 6: US4 Search | Phase 2 | US5+ |
| Phase 7: US5 Due Dates | Phase 2 | US6+ |
| Phase 8: US6 Recurring | Phase 2 | US7+ |
| Phase 9: US7 Stats | Phase 2 | Phase 10 |
| Phase 10: Polish | All stories | None |

### User Story Dependencies

- **US1 (Auth)**: After Phase 2 - No dependencies on other stories
- **US2 (CRUD)**: After Phase 2 - May integrate with US1 but should be independently testable
- **US3 (Org)**: After Phase 2 - Uses US2 task model, independently testable
- **US4 (Search)**: After Phase 2 - Uses US2 task model, independently testable
- **US5 (Due Dates)**: After Phase 2 - Uses US2 task model, independently testable
- **US6 (Recurring)**: After Phase 2 - Uses US2 task model, independently testable
- **US7 (Stats)**: After Phase 2 - Aggregates US2 data, independently testable

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 2

```bash
# Launch all backend models for User Story 2 together:
Task: "Create Task SQLModel with ALL fields in backend/models.py"
Task: "Create Pydantic schemas in backend/schemas.py"

# Launch all backend endpoints for User Story 2 together:
Task: "Create GET /tasks endpoint in backend/routes/tasks.py"
Task: "Create POST /tasks endpoint in backend/routes/tasks.py"
Task: "Create PUT /tasks/{task_id} endpoint in backend/routes/tasks.py"
Task: "Create DELETE /tasks/{task_id} endpoint in backend/routes/tasks.py"
Task: "Create PUT /tasks/{task_id}/complete endpoint in backend/routes/tasks.py"

# Launch all frontend components for User Story 2 together:
Task: "Create TaskForm component in frontend/components/tasks/TaskForm.tsx"
Task: "Create TaskItem component in frontend/components/tasks/TaskItem.tsx"
Task: "Create TaskList component in frontend/components/tasks/TaskList.tsx"
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Authentication)
4. Complete Phase 4: User Story 2 (Basic CRUD)
5. **STOP and VALIDATE**: Test User Stories 1+2 independently
6. Deploy/demo if ready - This is your MVP!

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Continue with remaining stories
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Auth)
   - Developer B: User Story 2 (CRUD)
   - Developer C: User Stories 3-4 (Organization)
   - Developer D: User Stories 5-7 (Advanced)
3. Stories complete and integrate independently

---

## Agent Mapping

| Agent | Tasks |
|-------|-------|
| database-schema | T015-T019 (Database foundation) |
| backend-generator | T020-T039 (Auth endpoints), T046-T052 (Task CRUD) |
| frontend-generator | T040-T045 (Auth UI), T053-T069 (Task UI) |
| auth-implementor | T020-T045 (All auth tasks) |
| api-router | T071-T075 (Search/Filter endpoints), T115-T122 (Stats endpoints) |

---

## Task Summary

| Phase | Task Count | Status |
|-------|------------|--------|
| Phase 1: Setup | 14 | COMPLETED |
| Phase 2: Foundational | 16 | COMPLETED |
| Phase 3: US1 Auth | 12 | COMPLETED |
| Phase 4: US2 CRUD | 16 | COMPLETED |
| Phase 5: US3 Org | 11 | COMPLETED |
| Phase 6: US4 Search | 15 | COMPLETED |
| Phase 7: US5 Due Dates | 15 | COMPLETED |
| Phase 8: US6 Recurring | 15 | COMPLETED |
| Phase 9: US7 Stats | 14 | COMPLETED |
| Phase 10: Polish | 14 | COMPLETED |

**Completed Tasks: 142**
**Remaining Tasks: 0**
**Total Tasks: 142**

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
