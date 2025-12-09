
from todo_cli.core import TaskManager
from todo_cli.storage import save_tasks, load_tasks
from todo_cli.ui import display_tasks, console
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align

task_manager = TaskManager()
task_manager.tasks = load_tasks()

# History for undo functionality
history = []

def print_menu():
    console.clear()
    heading = Align.center("[bold black]📝 TODO LIST MENU 📝[/bold black]")
    console.print(Panel(heading, style="bold white on cyan", padding=(1,4)))

    menu_table = Table.grid(padding=1)
    menu_table.add_column(justify="left")
    menu_table.add_row("[bold green]1[/bold green] ➤ Add Task")
    menu_table.add_row("[bold green]2[/bold green] ➤ List Tasks")
    menu_table.add_row("[bold green]3[/bold green] ➤ Edit Task")
    menu_table.add_row("[bold green]4[/bold green] ➤ Complete Task")
    menu_table.add_row("[bold green]5[/bold green] ➤ Delete Task")
    menu_table.add_row("[bold green]6[/bold green] ➤ Search Task")
    menu_table.add_row("[bold green]7[/bold green] ➤ Show Due Today Tasks")
    menu_table.add_row("[bold green]8[/bold green] ➤ Undo Last Action")
    menu_table.add_row("[bold green]0[/bold green] ➤ Exit")

    console.print(Panel(menu_table, border_style="bright_magenta"))

# =======================
# Task Operations
# =======================
def add_task_interactive():
    description = console.input("Enter description: ")
    priority_input = console.input("Enter priority (1-high, leave blank for none): ")
    priority = int(priority_input) if priority_input.isdigit() else None
    due_date_input = console.input("Enter due date (YYYY-MM-DD, leave blank for none): ")
    due_date = None
    if due_date_input:
        try:
            due_date = datetime.strptime(due_date_input, "%Y-%m-%d")
        except ValueError:
            console.print("[bold red]Invalid date format. Use YYYY-MM-DD.[/bold red]")
            return
    tags_input = console.input("Enter tags separated by commas (or leave blank): ")
    tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []

    task = task_manager.add_task(description, priority=priority, due_date=due_date, tags=tags)
    history.append(("add", task))
    save_tasks(task_manager.tasks)
    console.print("[bold green]✅ Task added![/bold green]")

def list_tasks_interactive():
    display_tasks(task_manager.get_all_tasks())

# =======================
# Description-based selection
# =======================
def select_task_by_description(action):
    desc_input = console.input(f"Enter task description to {action}: ").strip().lower()
    matches = [task for task in task_manager.get_all_tasks() if desc_input in task.description.lower()]

    if not matches:
        console.print(f"[bold red]❌ No task found matching '{desc_input}'[/bold red]")
        return None
    elif len(matches) == 1:
        return matches[0]
    else:
        console.print("[bold yellow]Multiple tasks found:[/bold yellow]")
        for t in matches:
            console.print(f"- {t.id[:8]} : {t.description}")
        chosen_id = console.input("Enter the ID of the task: ").strip()
        for t in matches:
            if t.id.startswith(chosen_id):
                return t
        console.print("[bold red]❌ Invalid ID entered.[/bold red]")
        return None

def edit_task_interactive():
    task = select_task_by_description("edit")
    if not task:
        return

    description = console.input(f"New description (leave blank to keep '{task.description}'): ") or task.description
    priority_input = console.input(f"New priority (leave blank to keep {task.priority}): ")
    priority = int(priority_input) if priority_input.isdigit() else task.priority
    due_date_input = console.input(f"New due date (YYYY-MM-DD, leave blank to keep {task.due_date}): ")
    due_date = task.due_date
    if due_date_input:
        try:
            due_date = datetime.strptime(due_date_input, "%Y-%m-%d")
        except ValueError:
            console.print("[bold red]Invalid date format. Keeping old date.[/bold red]")
    tags_input = console.input(f"New tags (comma-separated, leave blank to keep {task.tags}): ")
    tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else task.tags

    old_task = task_manager.update_task(task.id, new_description=task.description, completed=task.completed,
                                        priority=task.priority, due_date=task.due_date, tags=task.tags)
    task_manager.update_task(task.id, new_description=description, priority=priority, due_date=due_date, tags=tags)
    history.append(("edit", old_task))
    save_tasks(task_manager.tasks)
    console.print("[bold green]✅ Task updated![/bold green]")

def complete_task_interactive():
    task = select_task_by_description("complete")
    if task:
        task_manager.update_task(task.id, completed=True)
        history.append(("complete", task))
        save_tasks(task_manager.tasks)
        console.print("[bold green]✅ Task marked as completed![/bold green]")

def delete_task_interactive():
    task = select_task_by_description("delete")
    if task:
        task_manager.delete_task(task.id)
        history.append(("delete", task))
        save_tasks(task_manager.tasks)
        console.print("[bold green]🗑️ Task deleted![/bold green]")

def search_task_interactive():
    keyword = console.input("Enter search keyword: ")
    results = [task for task in task_manager.get_all_tasks() if keyword.lower() in task.description.lower()]
    display_tasks(results)

def due_today_tasks_interactive():
    today = datetime.today().date()
    results = [task for task in task_manager.get_all_tasks() if task.due_date and task.due_date.date() == today]
    display_tasks(results)

def undo_last_action():
    if not history:
        console.print("[bold yellow]Nothing to undo.[/bold yellow]")
        return
    action, task = history.pop()
    if action == "add":
        task_manager.delete_task(task.id)
    elif action == "delete":
        task_manager.tasks.append(task)
    elif action in ("edit", "complete"):
        task_manager.update_task(task.id, new_description=task.description, completed=task.completed,
                                 priority=task.priority, due_date=task.due_date, tags=task.tags)
    save_tasks(task_manager.tasks)
    console.print("[bold yellow]⏪ Last action undone![/bold yellow]")

# =======================
# Main loop
# =======================
while True:
    print_menu()
    choice = console.input("Select an option: ")

    if choice == "1":
        add_task_interactive()
    elif choice == "2":
        list_tasks_interactive()
    elif choice == "3":
        edit_task_interactive()
    elif choice == "4":
        complete_task_interactive()
    elif choice == "5":
        delete_task_interactive()
    elif choice == "6":
        search_task_interactive()
    elif choice == "7":
        due_today_tasks_interactive()
    elif choice == "8":
        undo_last_action()
    elif choice == "0":
        farewell = Align.center("[bold white on dark_green]👋 Bye! See you soon, keep smashing your tasks! 📝[/bold white on dark_green]", vertical="middle")
        console.print(Panel(farewell, padding=(2,4), border_style="bright_magenta"))
        break
    else:
        console.print("[bold red]Invalid option. Try again.[/bold red]")
