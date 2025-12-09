# Quickstart

This guide will help you get the Todo CLI application up and running.

## Prerequisites

-   Python 3.13+

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Create a virtual environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

3.  **Install dependencies**:
    ```bash
    pip install typer
    ```

## Running the Application

You can run the application using `typer`:

```bash
typer src/cli.py run [COMMAND] [ARGUMENTS]
```

For example, to add a new task:

```bash
typer src/cli.py run add "My first task" --priority High
```

To list all tasks:

```bash
typer src/cli.py run list
```
