# Tasks: Phase 3 AI-Powered Todo Chatbot

**Input**: Design documents from `/specs/001-chatbot-phase3/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/chat.md

**Organization**: Tasks are grouped by foundational infrastructure followed by prioritized user stories (US1: Task Creation, US2: Task Management, US3: History).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: US1 (Task Creation), US2 (Task Management), US3 (History)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure for MCP server and Chat routes
- [x] T002 Update `backend/pyproject.toml` with `openai-agents` and `mcp` dependencies
- [x] T003 Update `frontend/package.json` with `ai` dependency

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure required before any user story implementation

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [x] T004 [P] Create `Conversation` model in `backend/models.py`
- [x] T005 [P] Create `Message` model in `backend/models.py`
- [x] T006 Generate and run Alembic migration for conversation/message tables (Depends on T004, T005)
- [x] T007 [P] Initialize MCP server instance and directory structure in `backend/mcp_server/`
- [x] T008 [P] Implement JWT verification dependency in `backend/auth.py` and `backend/routes/chat.py`
- [x] T009 Create base `ChatRequest` and `ChatResponse` schemas in `backend/routes/chat.py`

**Checkpoint**: Foundation ready - user story implementation can now begin.

---

## Phase 3: User Story 1 - Natural Language Task Creation (Priority: P1) 🎯 MVP

**Goal**: Enable users to add tasks using natural language via the chatbot.

**Independent Test**: Send "Add buy milk" in chat and verify the task appears in the backend.

### Tests for User Story 1
- [x] T010 [P] [US1] Unit test for `add_task` MCP tool in `backend/tests/test_mcp.py`
- [x] T011 [P] [US1] Integration test for `/chat` endpoint with task creation intent in `backend/tests/test_chat.py`

### Implementation for User Story 1
- [x] T012 [P] [US1] Define `AddTaskInput` and `AddTaskOutput` schemas in `backend/mcp_server/schemas.py`
- [x] T013 [US1] Implement `add_task` tool handler in `backend/mcp_server/handlers.py`
- [x] T014 [US1] Register `add_task` tool with MCP server in `backend/mcp_server/tools.py`
- [x] T015 [US1] Configure TaskBot agent instructions and tool registration in `backend/routes/chat.py`
- [x] T016 [US1] Implement core POST `/api/{user_id}/chat` logic for new conversations and initial task creation
- [x] T017 [US1] Build initial `/chatbot` page in `frontend/app/chatbot/page.tsx` with basic input/send functionality

**Checkpoint**: User Story 1 works - tasks can be created via chat.

---

## Phase 4: User Story 2 - Task Retrieval and Management (Priority: P1)

**Goal**: Enable users to list, complete, delete, and update tasks via chat.

**Independent Test**: Ask "What are my tasks?" and then "Mark the first one as done".

### Tests for User Story 2
- [x] T018 [P] [US2] Unit tests for `list_tasks`, `complete_task`, `delete_task`, `update_task` in `backend/tests/test_mcp.py`

### Implementation for User Story 2
- [x] T019 [P] [US2] Define schemas for list, complete, delete, update tools in `backend/mcp_server/schemas.py`
- [x] T020 [US2] Implement `list_tasks` tool handler in `backend/mcp_server/handlers.py`
- [x] T021 [US2] Implement `complete_task` tool handler in `backend/mcp_server/handlers.py`
- [x] T022 [US2] Implement `delete_task` and `update_task` tool handlers in `backend/mcp_server/handlers.py`
- [x] T023 [US2] Register management tools with MCP server in `backend/mcp_server/tools.py`
- [x] T024 [US2] Update TaskBot agent with instructions for task management and identification by context

**Checkpoint**: User Story 2 works - full CRUD management of tasks via chat.

---

## Phase 5: User Story 3 - Conversational History & Context (Priority: P2)

**Goal**: Persistent chat history and context-aware responses.

**Independent Test**: Refresh /chatbot page and see previous messages. Use "it" to refer to previous tasks.

### Tests for User Story 3
- [x] T025 [P] [US3] Integration test for conversation retrieval and context-aware turn in `backend/tests/test_chat.py`

### Implementation for User Story 3
- [x] T026 [US3] Implement `get_conversation_messages` and `save_message` persistence logic in `backend/routes/chat.py`
- [x] T027 [US3] Add sliding window message history loading in `/chat` endpoint logic
- [x] T028 [US3] Implement conversation loading on mount in `frontend/app/chatbot/page.tsx`
- [x] T029 [US3] Refine Chat UI to display full history with proper roles (user/assistant styling)

**Checkpoint**: User Story 3 works - chat feels like a persistent assistant.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: UX improvements, navigation, and final validation.

- [x] T030 Add `/chatbot` link to `frontend/components/navigation.tsx`
- [x] T031 Implement streaming responses using Vercel AI SDK `useChat` hook in `frontend/app/chatbot/page.tsx`
- [x] T032 Add loading states and animated "bot typing" indicator
- [x] T033 Implementation walkthrough and verify Phase 2 regression
- [x] T034 Run `quickstart.md` validation and final README update

---

## Dependencies & Execution Order

### Phase Dependencies
- **Phase 1-2**: Blocking foundation. Must complete tables and MCP initialization.
- **Phase 3 (US1)**: First MVP increment.
- **Phase 4 (US2)**: Extends US1 with more tools.
- **Phase 5 (US3)**: Adds persistence and UX refinement.

### Parallel Opportunities
- Database models (T004, T005) can be created simultaneously.
- MCP schemas (T012, T019) can be defined in parallel once the structure is there.
- Once the `/chat` endpoint core logic (T016) is stable, Frontend (T017) and more MCP tools (T020-T022) can proceed in parallel.
