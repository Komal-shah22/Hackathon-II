import typer
from typing_extensions import Annotated
from todo_cli.core import task_manager
from todo_cli import storage
from todo_cli import ui
from datetime import datetime
from typing import Optional, List

app = typer.Typer()

# Load tasks at the start of the application
task_manager.tasks = storage.load_tasks()

@app.command()
def add(
    description: str,
    priority: Annotated[Optional[int], typer.Option(help="Priority level for the task (e.g., 1 for high).")] = None,
    due_date: Annotated[Optional[str], typer.Option(help="Due date for the task (YYYY-MM-DD).")] = None,
    tags: Annotated[Optional[List[str]], typer.Option("--tag", "-t", help="Tag to add to the task. Can be used multiple times.")] = None,
):
    """
    Add a new task.
    """
    parsed_due_date = None
    if due_date:
        try:
            parsed_due_date = datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            ui.console.print("[bold red]Error:[/bold red] Invalid due date format. Please use YYYY-MM-DD.")
            raise typer.Exit(code=1)

    task = task_manager.add_task(description, priority=priority, due_date=parsed_due_date, tags=tags)
    ui.console.print(f"[bold green]✅ Task added:[/bold green] [cyan]{task.description}[/cyan] (ID: [dim]{task.id[:4]}...[/dim])")
    storage.save_tasks(task_manager.tasks)

@app.command()
def list(
    tag: Annotated[Optional[str], typer.Option(help="Filter tasks by tag.")] = None,
    priority: Annotated[Optional[int], typer.Option(help="Filter tasks by priority level.")] = None,
    status: Annotated[Optional[bool], typer.Option(help="Filter tasks by completion status (true/false).")] = None,
):
    """
    List all tasks, optionally filtered.
    """
    tasks = task_manager.get_all_tasks(tag=tag, priority=priority, completed=status)
    ui.display_tasks(tasks)

@app.command()
def search(query: str):
    """
    Search tasks by matching text in their description.
    """
    matching_tasks = task_manager.search_tasks(query)
    ui.console.print(f"[bold blue]🔍 Search results for '[cyan]{query}[/cyan]':[/bold blue]")
    ui.display_tasks(matching_tasks)


@app.command()
def edit(
    task_id: str,
    description: Annotated[Optional[str], typer.Option(help="New description for the task.")] = None,
    completed: Annotated[Optional[bool], typer.Option(help="Mark task as completed or not.")] = None,
    priority: Annotated[Optional[int], typer.Option(help="New priority level for the task.")] = None,
    due_date: Annotated[Optional[str], typer.Option(help="New due date for the task (YYYY-MM-DD).")] = None,
    tags: Annotated[Optional[List[str]], typer.Option("--tag", "-t", help="Tags to set for the task. Clears existing tags if not provided.")] = None,
):
    """
    Edit an existing task.
    """
    parsed_due_date = None
    if due_date:
        try:
            parsed_due_date = datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            ui.console.print("[bold red]Error:[/bold red] Invalid due date format. Please use YYYY-MM-DD.")
            raise typer.Exit(code=1)

    updated_task = task_manager.update_task(
        task_id,
        new_description=description,
        completed=completed,
        priority=priority,
        due_date=parsed_due_date,
        tags=tags
    )
    if updated_task:
        ui.console.print(f"[bold green]✅ Task updated:[/bold green] [cyan]{updated_task.description}[/cyan] (ID: [dim]{updated_task.id[:4]}...[/dim])")
        storage.save_tasks(task_manager.tasks)
    else:
        ui.console.print(f"[bold red]Error:[/bold red] Task with ID '[dim]{task_id}[/dim]' not found.")

@app.command()
def complete(task_id: str):
    """
    Mark a task as completed.
    """
    updated_task = task_manager.update_task(task_id, completed=True)
    if updated_task:
        ui.console.print(f"[bold green]✅ Task '[cyan]{updated_task.description}[/cyan]' marked as completed.[/bold green]")
        storage.save_tasks(task_manager.tasks)
    else:
        ui.console.print(f"[bold red]Error:[/bold red] Task with ID '[dim]{task_id}[/dim]' not found.")

@app.command()
def delete(task_id: str):
    """
    Delete a task by its ID.
    """
    if task_manager.delete_task(task_id):
        ui.console.print(f"[bold green]🗑️ Task with ID '[dim]{task_id}[/dim]' deleted.[/bold green]")
        storage.save_tasks(task_manager.tasks)
    else:
        ui.console.print(f"[bold red]Error:[/bold red] Task with ID '[dim]{task_id}[/dim]' not found.")

if __name__ == "__main__":
    app()
