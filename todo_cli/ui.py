from typing import List
from rich.console import Console
from rich.table import Table
from rich.text import Text
from todo_cli.models import Task

console = Console()

def display_tasks(tasks: List[Task]):
    """
    Displays a list of tasks in a user-friendly table format using rich.
    """
    if not tasks:
        console.print("[bold yellow]No tasks found.[/bold yellow]")
        return

    table = Table(title="Your Tasks", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=12)
    table.add_column("Done", justify="center")
    table.add_column("Priority", justify="center")
    table.add_column("Description", style="cyan")
    table.add_column("Due Date", style="green")

    for task in tasks:
        # Determine status display
        if task.completed:
            status_display = Text("✓", style="bold green")
            description_style = "dim green"
        else:
            status_display = Text("✗", style="bold red")
            description_style = "cyan"
        
        # Determine priority display
        priority_display = ""
        if task.priority is not None:
            if task.priority <= 2:
                priority_display = Text(f"P{task.priority}", style="bold red")
            elif task.priority <= 5:
                priority_display = Text(f"P{task.priority}", style="bold yellow")
            else:
                priority_display = Text(f"P{task.priority}", style="dim white")

        due_date_display = Text(task.due_date.strftime("%Y-%m-%d"), style="green") if task.due_date else ""

        table.add_row(
            Text(task.id[:8], style="dim"),
            status_display,
            priority_display,
            Text(task.description, style=description_style),
            due_date_display
        )
    
    console.print(table)
