# Tasks: 001-advanced-task-management

**Input**: Design documents from `/specs/001-advanced-task-management/`
**Prerequisites**: plan.md, spec.md

## Path Conventions

- Project Root: `.`
- Source Code: `todo_cli/`
- Tests: `tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for the Python CLI application.

- [x] T001 Create the initial project directory structure: `todo_cli/`, `tests/`
- [x] T002 Initialize a Python project with a `pyproject.toml` file
- [x] T003 [P] Add and install dependencies (`typer`, `rich`, `pytest`) into the project environment

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data models and CLI entrypoint that MUST be complete before ANY user story can be implemented.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [x] T004 Define the core `Task` data structure in `todo_cli/models.py`
- [x] T005 Create the main CLI application entrypoint in `todo_cli/cli.py` using `typer`
- [x] T006 [P] Implement placeholder functions for data persistence in `todo_cli/storage.py` (`load_tasks`, `save_tasks`)
- [x] T007 [P] Implement the core task management logic class/module in `todo_cli/core.py` with an in-memory list

**Checkpoint**: Foundation ready - user story implementation can now begin.

---

## Phase 3: User Story 1 - Core Task Management (Priority: P1) 🎯 MVP

**Goal**: As a user, I want to add, view, edit, and delete tasks so I can manage my to-do list.

**Independent Test**: A user can add a task, see it with the `list` command, modify it with the `edit` command, and remove it with the `delete` command. All changes are reflected in subsequent `list` commands.

### Implementation for User Story 1

- [x] T008 [US1] Implement `add_task` logic in `todo_cli/core.py`
- [x] T009 [US1] Create the `add` command in `todo_cli/cli.py` that calls `core.add_task`
- [x] T010 [US1] Implement `get_all_tasks` logic in `todo_cli/core.py`
- [x] T011 [US1] Create the `list` command in `todo_cli/cli.py` to display task descriptions
- [x] T012 [US1] Implement `update_task` logic in `todo_cli/core.py`
- [x] T013 [US1] Create the `edit` command in `todo_cli/cli.py` that calls `core.update_task`
- [x] T014 [US1] Implement `delete_task` logic in `todo_cli/core.py`
- [x] T015 [US1] Create the `delete` command in `todo_cli/cli.py` that calls `core.delete_task`

**Checkpoint**: At this point, User Story 1 should be fully functional using in-memory storage.

---

## Phase 4: User Story 2 - Data Persistence (Priority: P2)

**Goal**: As a user, I want my tasks to be saved between sessions so that my data is not lost.

**Independent Test**: A user can add a task, close the application, reopen it, and the previously added task is still present in the `list` command output.

### Implementation for User Story 2

- [x] T016 [US2] Implement `save_tasks` in `todo_cli/storage.py` to serialize the task list to a JSON file
- [x] T017 [US2] Implement `load_tasks` in `todo_cli/storage.py` to deserialize tasks from a JSON file
- [x] T018 [US2] Integrate `load_tasks` at the start of the CLI app in `todo_cli/cli.py`
- [x] T019 [US2] Integrate `save_tasks` after every command that modifies data (`add`, `edit`, `delete`) in `todo_cli/cli.py`
- [x] T020 [US2] Implement atomic writes in `todo_cli/storage.py` by writing to a temporary file before renaming

**Checkpoint**: At this point, all core task operations persist between application runs.

---

## Phase 5: User Story 3 - Task Metadata (Priority: P3)

**Goal**: As a user, I want to mark tasks as complete and add priority levels and deadlines.

**Independent Test**: A user can add a task with a priority and deadline, mark it as complete, and see all metadata reflected in the `list` view.

### Implementation for User Story 3

- [x] T021 [US3] Extend the `Task` model in `todo_cli/models.py` to include `completed` (bool), `priority` (int), and `due_date` (str)
- [x] T022 [US3] [P] Update the `add` and `edit` commands in `todo_cli/cli.py` to accept `--priority` and `--due-date` options
- [x] T023 [US3] Create the `complete` command in `todo_cli/cli.py` to mark a task as done
- [x] T024 [US3] Update the `list` command's display logic in `todo_cli/cli.py` to show the new metadata fields

**Checkpoint**: Users can now manage task completion status and other metadata.

---

## Phase 6: User Story 4 - UX & CLI Polish (Priority: P3)

**Goal**: As a user, I want a beautiful and user-friendly CLI with clear feedback.

**Independent Test**: The `list` command displays a formatted table with colors. All commands provide clear, user-friendly confirmation messages.

### Implementation for User Story 4

- [x] T025 [US4] [P] Create a dedicated `display_tasks` function in `todo_cli/ui.py`
- [x] T026 [US4] Refactor the `list` command in `todo_cli/cli.py` to use `rich.table.Table` via `ui.display_tasks` for clean output
- [x] T027 [US4] Add color-coding to the table output in `todo_cli/ui.py` based on task priority or completion status
- [x] T028 [US4] Add user-friendly confirmation messages (e.g., "✅ Task added:", "❌ Task not found.") to all commands in `todo_cli/cli.py`

**Checkpoint**: The application is now more visually appealing and user-friendly.

---

## Phase 7: User Story 5 - Advanced Organization (Priority: P4)

**Goal**: As a user, I want to tag my tasks and search or filter them.

**Independent Test**: A user can add tags to a task, then filter the `list` view to show only tasks with a specific tag or priority.

### Implementation for User Story 5

- [x] T029 [US5] Extend `Task` model in `todo_cli/models.py` with a list of `tags`
- [x] T030 [US5] [P] Update `add`/`edit` commands in `todo_cli/cli.py` to support adding/modifying tags
- [x] T031 [US5] Enhance the `list` command in `todo_cli/cli.py` to accept `--tag`, `--priority`, or `--status` filter flags
- [x] T032 [US5] Implement the filtering logic within `core.get_all_tasks` or a new `core.get_filtered_tasks` function
- [x] T033 [US5] [P] Create a `search` command in `todo_cli/cli.py` to find tasks with matching text in their description

**Checkpoint**: Users can now effectively search and filter their tasks.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements that affect multiple user stories.

- [x] T034 [P] Write unit tests for core logic in `tests/test_core.py`
- [x] T035 [P] Write unit tests for storage logic in `tests/test_storage.py`
- [x] T036 [P] Add docstrings and type hints to all functions and classes
- [x] T037 [P] Create/update the `README.md` with installation and usage instructions

---

## Dependencies & Execution Order

- **Phase 1 (Setup)** -> **Phase 2 (Foundational)** -> **All User Stories**
- User stories can largely be implemented sequentially as ordered above, as they build upon each other.
- **US4 (UX Polish)** can be done any time after **US1 (Core CRUD)**.
- **US5 (Advanced Org)** should follow **US3 (Metadata)**.

## Implementation Strategy

1. **MVP First**: Complete Phases 1, 2, and 3 to have a functional, in-memory TODO app.
2. **Incremental Delivery**:
   - Add Phase 4 (Persistence) for a durable app.
   - Add Phase 5 (Metadata) for more powerful organization.
   - Add Phase 6 (UX Polish) for a better user experience.
   - Add Phase 7 (Advanced Org) for advanced features.
   - Complete Phase 8 (Polish) for a production-ready application.
