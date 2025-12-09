# CLI Commands

This document defines the command-line interface for the Todo application.

## General Usage

```bash
todo [COMMAND] [ARGUMENTS]
```

## Commands

### `add`

Adds a new task.

-   **Usage**: `todo add <title> [OPTIONS]`
-   **Arguments**:
    -   `<title>`: The title of the task (required).
-   **Options**:
    -   `--description TEXT`: A description of the task.
    -   `--priority [High|Medium|Low|None]`: The priority of the task.
    -   `--tags TEXT`: A comma-separated list of tags.
    -   `--due-date TEXT`: The due date in YYYY-MM-DD format.

### `update`

Updates an existing task.

-   **Usage**: `todo update <task_id> [OPTIONS]`
-   **Arguments**:
    -   `<task_id>`: The ID of the task to update (required).
-   **Options**:
    -   `--title TEXT`: The new title of the task.
    -   `--description TEXT`: The new description of the task.
    -   `--priority [High|Medium|Low|None]`: The new priority of the task.
    -   `--tags TEXT`: A new comma-separated list of tags (will overwrite existing tags).
    -   `--due-date TEXT`: The new due date in YYYY-MM-DD format.

### `delete`

Deletes a task.

-   **Usage**: `todo delete <task_id>`
-   **Arguments**:
    -   `<task_id>`: The ID of the task to delete (required).

### `complete`

Marks a task as complete.

-   **Usage**: `todo complete <task_id>`
-   **Arguments**:
    -   `<task_id>`: The ID of the task to mark as complete (required).

### `uncomplete`

Marks a task as not complete.

-   **Usage**: `todo uncomplete <task_id>`
-   **Arguments**:
    -   `<task_id>`: The ID of the task to mark as not complete (required).

### `list`

Lists all tasks.

-   **Usage**: `todo list [OPTIONS]`
-   **Options**:
    -   `--search TEXT`: Search for tasks by keyword.
    -   `--filter-status [pending|complete]`: Filter tasks by status.
    -   `--filter-priority [High|Medium|Low|None]`: Filter tasks by priority.
    -   `--filter-tag TEXT`: Filter tasks by tag.
    -   `--filter-due-date TEXT`: Filter tasks by due date.
    -   `--sort-by [due_date|priority|title]`: Sort tasks by a specific field.
    -   `--sort-order [asc|desc]`: The sort order.
