# TODO CLI Application

A highly polished, feature-rich command-line interface (CLI) application for managing your to-do tasks.

## Features

- Add tasks with descriptions, priority, due dates, and tags.
- List all tasks, with filtering options by tag, priority, and completion status.
- Edit existing tasks (description, completion status, priority, due date, tags).
- Mark tasks as complete.
- Delete tasks.
- Search tasks by keywords in their description.
- Persistent storage using a JSON file.
- User-friendly output with color-coding via `rich`.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/todo-cli-app.git
    cd todo-cli-app
    ```

2.  **Install dependencies:**
    It's recommended to use a virtual environment.
    ```bash
    python -m venv venv
    .\venv\Scripts\activate   # On Windows
    # source venv/bin/activate  # On macOS/Linux

    pip install -e .
    # This will install typer, rich, and pytest, and make the `todo` command available.
    ```
    *(Note: The `pip install -e .` command requires the `name` and `packages` configuration in `pyproject.toml` or `setup.py` to make the package discoverable and installable in editable mode.)*

## Usage

The main command for the application is `todo`.

### Add a Task

```bash
todo add "Buy groceries" --priority 1 --due-date 2025-12-31 --tag shopping --tag urgent
```
Output:
```
✅ Task added: Buy groceries (ID: xxxx...)
```

### List Tasks

```bash
todo list
```
Output:
```
╭───────────────── Your Tasks ─────────────────╮
│ ID       Done Priority Description    Due Date │
├──────────────────────────────────────────────┤
│ xxxx...  ✗    P1       Buy groceries  2025-12-31 │
│ yyyy...  ✓             Finish report  2025-12-15 │
╰──────────────────────────────────────────────╯
```

**Filter by Tag:**
```bash
todo list --tag shopping
```

**Filter by Priority:**
```bash
todo list --priority 1
```

**Filter by Status (completed/uncompleted):**
```bash
todo list --status true
```
```bash
todo list --status false
```

### Edit a Task

(You'll need the Task ID from the `list` command)
```bash
todo edit <TASK_ID> --description "Buy milk and bread" --completed true --priority 2
```
Output:
```
✅ Task updated: Buy milk and bread (ID: xxxx...)
```

### Mark a Task as Complete

```bash
todo complete <TASK_ID>
```
Output:
```
✅ Task 'Buy milk and bread' marked as completed.
```

### Delete a Task

```bash
todo delete <TASK_ID>
```
Output:
```
🗑️ Task with ID 'xxxx...' deleted.
```

### Search Tasks

```bash
todo search "report"
```
Output:
```
🔍 Search results for 'report':
╭───────────────── Your Tasks ─────────────────╮
│ ID       Done Priority Description    Due Date │
├──────────────────────────────────────────────┤
│ yyyy...  ✓             Finish report  2025-12-15 │
╰──────────────────────────────────────────────╯
```

## Development

To run tests:
```bash
pytest
```
"# Hackathon-II" 
"# Hackathon-II" 
