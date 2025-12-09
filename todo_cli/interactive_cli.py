# from todo_cli.core import task_manager
# from todo_cli.storage import save_tasks, load_tasks
# from todo_cli import ui
# from datetime import datetime

# # Load existing tasks
# task_manager.tasks = load_tasks()

# def input_date(prompt: str):
#     date_str = input(prompt)
#     if not date_str.strip():
#         return None
#     try:
#         return datetime.strptime(date_str, "%Y-%m-%d")
#     except ValueError:
#         print("Invalid date format. Use YYYY-MM-DD.")
#         return input_date(prompt)

# def input_priority(prompt: str):
#     p = input(prompt)
#     if not p.strip():
#         return None
#     try:
#         return int(p)
#     except ValueError:
#         print("Priority must be a number.")
#         return input_priority(prompt)

# def input_tags():
#     tags_str = input("Enter tags separated by commas (or leave blank): ")
#     return [t.strip() for t in tags_str.split(",") if t.strip()]

# while True:
#     print("\n==============================")
#     print("       TODO LIST MENU")
#     print("==============================")
#     print("1. Add Task")
#     print("2. List Tasks")
#     print("3. Edit Task")
#     print("4. Complete Task")
#     print("5. Delete Task")
#     print("6. Search Task")
#     print("0. Exit")

#     choice = input("Select an option: ").strip()

#     if choice == "1":
#         desc = input("Enter description: ")
#         priority = input_priority("Enter priority (1-high, leave blank for none): ")
#         due_date = input_date("Enter due date (YYYY-MM-DD, leave blank for none): ")
#         tags = input_tags()
#         task_manager.add_task(desc, priority=priority, due_date=due_date, tags=tags)
#         save_tasks(task_manager.tasks)
#         print("✅ Task added!")

#     elif choice == "2":
#         tasks = task_manager.get_all_tasks()
#         ui.display_tasks(tasks)

#     elif choice == "3":
#         task_id = input("Enter task ID to edit: ")
#         task = task_manager.get_task_by_id(task_id)
#         if not task:
#             print("Task not found.")
#             continue
#         new_desc = input(f"New description (leave blank to keep '{task.description}'): ") or None
#         new_priority = input_priority(f"New priority (leave blank to keep '{task.priority}'): ")
#         new_due = input_date(f"New due date (leave blank to keep '{task.due_date}'): ")
#         new_tags = input_tags() or None
#         completed_input = input(f"Mark completed? (y/n, leave blank to keep '{task.completed}'): ").lower()
#         completed = None
#         if completed_input == "y":
#             completed = True
#         elif completed_input == "n":
#             completed = False
#         task_manager.update_task(task_id, new_description=new_desc, priority=new_priority,
#                                  due_date=new_due, tags=new_tags, completed=completed)
#         save_tasks(task_manager.tasks)
#         print("✅ Task updated!")

#     elif choice == "4":
#         task_id = input("Enter task ID to complete: ")
#         task = task_manager.update_task(task_id, completed=True)
#         if task:
#             save_tasks(task_manager.tasks)
#             print(f"✅ Task '{task.description}' marked as completed.")
#         else:
#             print("Task not found.")

#     elif choice == "5":
#         task_id = input("Enter task ID to delete: ")
#         if task_manager.delete_task(task_id):
#             save_tasks(task_manager.tasks)
#             print("🗑️ Task deleted.")
#         else:
#             print("Task not found.")

#     elif choice == "6":
#         keyword = input("Enter search keyword: ")
#         results = task_manager.search_tasks(keyword)
#         ui.display_tasks(results)

#     elif choice == "0":
#         print("Exiting... 👋")
#         break

#     else:
#         print("Invalid option. Try again.")




# from todo_cli.core import TaskManager
# from todo_cli.storage import save_tasks, load_tasks
# from todo_cli.ui import display_tasks
# from datetime import datetime

# task_manager = TaskManager()
# task_manager.tasks = load_tasks()

# # To keep last deleted/completed task for undo
# last_action = None
# last_task = None

# def select_task(tasks):
#     """Let user select task by number instead of UUID."""
#     if not tasks:
#         print("No tasks available.")
#         return None
#     for i, task in enumerate(tasks, 1):
#         status = "✓" if task.completed else "✗"
#         print(f"{i}. [{status}] {task.description} (P{task.priority if task.priority else '-'})")
#     try:
#         choice = int(input("Select task number: "))
#         if 1 <= choice <= len(tasks):
#             return tasks[choice - 1]
#     except ValueError:
#         pass
#     print("Invalid selection.")
#     return None

# while True:
#     print("\n==============================")
#     print("       TODO LIST MENU")
#     print("==============================")
#     print("1. Add Task")
#     print("2. List Tasks")
#     print("3. Edit Task")
#     print("4. Complete Task")
#     print("5. Delete Task")
#     print("6. Search Task")
#     print("7. Show Due Today Tasks")
#     print("8. Undo Last Action")
#     print("0. Exit")
    
#     choice = input("Select an option: ")

#     if choice == "1":
#         desc = input("Enter description: ")
#         priority = input("Enter priority (1-high, leave blank for none): ")
#         priority = int(priority) if priority.strip().isdigit() else None
#         due_date = input("Enter due date (YYYY-MM-DD, leave blank for none): ")
#         if due_date:
#             try:
#                 due_date = datetime.strptime(due_date, "%Y-%m-%d")
#             except ValueError:
#                 print("Invalid date format. Use YYYY-MM-DD.")
#                 due_date = None
#         tags = input("Enter tags separated by commas (or leave blank): ")
#         tags = [t.strip() for t in tags.split(",")] if tags else []
#         notes = input("Optional notes (leave blank if none): ").strip()
#         task_manager.add_task(desc, priority=priority, due_date=due_date, tags=tags)
#         print("✅ Task added!")
#         save_tasks(task_manager.tasks)

#     elif choice == "2":
#         display_tasks(task_manager.tasks)

#     elif choice == "3":
#         task = select_task(task_manager.tasks)
#         if task:
#             new_desc = input(f"New description (leave blank to keep '{task.description}'): ").strip()
#             new_priority = input(f"New priority (leave blank to keep '{task.priority}'): ").strip()
#             new_priority = int(new_priority) if new_priority.isdigit() else task.priority
#             new_due = input(f"New due date YYYY-MM-DD (leave blank to keep '{task.due_date}'): ").strip()
#             if new_due:
#                 try:
#                     new_due = datetime.strptime(new_due, "%Y-%m-%d")
#                 except ValueError:
#                     print("Invalid date format. Keeping old due date.")
#                     new_due = task.due_date
#             else:
#                 new_due = task.due_date
#             new_tags = input(f"New tags (comma separated, leave blank to keep '{', '.join(task.tags)}'): ").strip()
#             new_tags = [t.strip() for t in new_tags.split(",")] if new_tags else task.tags
#             task.description = new_desc if new_desc else task.description
#             task.priority = new_priority
#             task.due_date = new_due
#             task.tags = new_tags
#             print("✅ Task updated!")
#             save_tasks(task_manager.tasks)

#     elif choice == "4":
#         task = select_task(task_manager.tasks)
#         if task:
#             task.completed = True
#             last_action = "complete"
#             last_task = task
#             print(f"✅ Task '{task.description}' marked as completed.")
#             save_tasks(task_manager.tasks)

#     elif choice == "5":
#         task = select_task(task_manager.tasks)
#         if task:
#             task_manager.delete_task(task.id)
#             last_action = "delete"
#             last_task = task
#             print(f"🗑️ Task '{task.description}' deleted.")
#             save_tasks(task_manager.tasks)

#     elif choice == "6":
#         keyword = input("Enter search keyword: ").strip()
#         filtered = [t for t in task_manager.tasks if keyword.lower() in t.description.lower() or keyword in t.tags]
#         display_tasks(filtered)

#     elif choice == "7":
#         today = datetime.now().date()
#         due_today = [t for t in task_manager.tasks if t.due_date and t.due_date.date() == today]
#         display_tasks(due_today)

#     elif choice == "8":
#         if last_action and last_task:
#             if last_action == "delete":
#                 task_manager.tasks.append(last_task)
#                 print(f"✅ Restored deleted task '{last_task.description}'.")
#             elif last_action == "complete":
#                 last_task.completed = False
#                 print(f"✅ Reverted completion of task '{last_task.description}'.")
#             save_tasks(task_manager.tasks)
#             last_action = None
#             last_task = None
#         else:
#             print("No action to undo.")

#     elif choice == "0":
#         print("Exiting... 👋")
#         break

#     else:
#         print("Invalid option. Try again.")






# from datetime import datetime, date
# from rich.console import Console
# from rich.table import Table
# from rich.panel import Panel
# from rich.prompt import Prompt
# from rich.text import Text
# from todo_cli.core import TaskManager
# from todo_cli.storage import save_tasks, load_tasks

# console = Console()
# task_manager = TaskManager()
# task_manager.tasks = load_tasks()

# # Simple undo stack
# undo_stack = []

# def print_menu():
#     console.clear()
#     console.print(Panel.fit(
#         "[bold magenta]📝 TODO LIST MENU 📝[/bold magenta]",
#         style="bold white on dark_blue",
#         padding=(1,2)
#     ))
#     menu_table = Table.grid(padding=1)
#     menu_table.add_column(justify="center")
#     menu_table.add_row("[bold green]1[/bold green] ➤ Add Task")
#     menu_table.add_row("[bold green]2[/bold green] ➤ List Tasks")
#     menu_table.add_row("[bold green]3[/bold green] ➤ Edit Task")
#     menu_table.add_row("[bold green]4[/bold green] ➤ Complete Task")
#     menu_table.add_row("[bold green]5[/bold green] ➤ Delete Task")
#     menu_table.add_row("[bold green]6[/bold green] ➤ Search Task")
#     menu_table.add_row("[bold green]7[/bold green] ➤ Show Due Today Tasks")
#     menu_table.add_row("[bold green]8[/bold green] ➤ Undo Last Action")
#     menu_table.add_row("[bold green]0[/bold green] ➤ Exit")
#     console.print(Panel(menu_table, border_style="bright_magenta"))

# def display_tasks(tasks):
#     if not tasks:
#         console.print("[bold yellow]No tasks found.[/bold yellow]")
#         return

#     table = Table(title="📋 Your Tasks", show_header=True, header_style="bold magenta")
#     table.add_column("ID", style="dim", width=8)
#     table.add_column("Done", justify="center")
#     table.add_column("Priority", justify="center")
#     table.add_column("Description", style="cyan")
#     table.add_column("Due Date", style="green")
#     table.add_column("Tags", style="magenta")

#     for task in tasks:
#         status_display = "✓" if task.completed else "✗"
#         desc_style = "dim green" if task.completed else "cyan"

#         # Priority colors
#         if task.priority is None:
#             priority_display = ""
#         elif task.priority <= 2:
#             priority_display = Text(f"P{task.priority}", style="bold red")
#         elif task.priority <= 5:
#             priority_display = Text(f"P{task.priority}", style="bold yellow")
#         else:
#             priority_display = Text(f"P{task.priority}", style="dim white")

#         # Due date color
#         due_date_display = ""
#         if task.due_date:
#             if task.due_date.date() == date.today():
#                 due_date_display = Text(task.due_date.strftime("%Y-%m-%d"), style="bold red")
#             else:
#                 due_date_display = task.due_date.strftime("%Y-%m-%d")

#         tags_display = ", ".join(task.tags) if task.tags else ""

#         table.add_row(task.id[:8], status_display, str(priority_display), Text(task.description, style=desc_style), str(due_date_display), tags_display)

#     console.print(table)

# def add_task():
#     desc = Prompt.ask("[bold cyan]Enter description[/bold cyan]")
#     priority_str = Prompt.ask("[bold cyan]Enter priority (1-high, leave blank for none)[/bold cyan]", default="")
#     priority = int(priority_str) if priority_str.isdigit() else None
#     due_date_str = Prompt.ask("[bold cyan]Enter due date (YYYY-MM-DD, leave blank for none)[/bold cyan]", default="")
#     due_date = None
#     if due_date_str:
#         try:
#             due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
#         except ValueError:
#             console.print("[bold red]Invalid date format. Use YYYY-MM-DD.[/bold red]")
#     tags_str = Prompt.ask("[bold cyan]Enter tags separated by commas (or leave blank)[/bold cyan]", default="")
#     tags = [tag.strip() for tag in tags_str.split(",")] if tags_str else []

#     task = task_manager.add_task(desc, priority=priority, due_date=due_date, tags=tags)
#     undo_stack.append(("delete", task.id))  # Save for undo
#     save_tasks(task_manager.tasks)
#     console.print(f"[bold green]✅ Task '{desc}' added![/bold green]")

# def list_tasks():
#     display_tasks(task_manager.get_all_tasks())

# def edit_task():
#     task_id = Prompt.ask("[bold cyan]Enter task ID to edit[/bold cyan]")
#     task = task_manager.get_task_by_id(task_id)
#     if not task:
#         console.print("[bold red]Task not found.[/bold red]")
#         return

#     new_desc = Prompt.ask(f"[bold cyan]Enter new description (leave blank to keep '{task.description}')[/bold cyan]", default=task.description)
#     new_priority_str = Prompt.ask(f"[bold cyan]Enter new priority (leave blank to keep {task.priority})[/bold cyan]", default=str(task.priority) if task.priority else "")
#     new_priority = int(new_priority_str) if new_priority_str.isdigit() else task.priority
#     new_due_date_str = Prompt.ask(f"[bold cyan]Enter new due date (YYYY-MM-DD, leave blank to keep {task.due_date})[/bold cyan]", default=task.due_date.strftime("%Y-%m-%d") if task.due_date else "")
#     new_due_date = datetime.strptime(new_due_date_str, "%Y-%m-%d") if new_due_date_str else task.due_date
#     new_tags_str = Prompt.ask(f"[bold cyan]Enter new tags separated by commas (leave blank to keep {', '.join(task.tags)})[/bold cyan]", default=",".join(task.tags))
#     new_tags = [t.strip() for t in new_tags_str.split(",")] if new_tags_str else task.tags

#     # Save undo
#     undo_stack.append(("edit", task.to_dict()))
#     task_manager.update_task(task_id, new_description=new_desc, priority=new_priority, due_date=new_due_date, tags=new_tags)
#     save_tasks(task_manager.tasks)
#     console.print(f"[bold green]✅ Task '{new_desc}' updated![/bold green]")

# def complete_task():
#     task_id = Prompt.ask("[bold cyan]Enter task ID to complete[/bold cyan]")
#     task = task_manager.update_task(task_id, completed=True)
#     if task:
#         undo_stack.append(("incomplete", task_id))
#         save_tasks(task_manager.tasks)
#         console.print(f"[bold green]✅ Task '{task.description}' marked as completed.[/bold green]")
#     else:
#         console.print("[bold red]Task not found.[/bold red]")

# def delete_task():
#     task_id = Prompt.ask("[bold cyan]Enter task ID to delete[/bold cyan]")
#     task = task_manager.get_task_by_id(task_id)
#     if task and task_manager.delete_task(task_id):
#         undo_stack.append(("add", task))  # save task for undo
#         save_tasks(task_manager.tasks)
#         console.print(f"[bold green]🗑️ Task '{task.description}' deleted.[/bold green]")
#     else:
#         console.print("[bold red]Task not found.[/bold red]")

# def search_task():
#     keyword = Prompt.ask("[bold cyan]Enter search keyword[/bold cyan]")
#     tasks = task_manager.search_tasks(keyword)
#     display_tasks(tasks)

# def due_today_tasks():
#     today_tasks = [task for task in task_manager.tasks if task.due_date and task.due_date.date() == date.today()]
#     display_tasks(today_tasks)

# def undo_last_action():
#     if not undo_stack:
#         console.print("[bold yellow]Nothing to undo.[/bold yellow]")
#         return
#     action = undo_stack.pop()
#     if action[0] == "delete":
#         task_manager.delete_task(action[1])
#     elif action[0] == "add":
#         task_manager.add_task(**action[1].to_dict())
#     elif action[0] == "edit":
#         task_manager.update_task(action[1]["id"],
#                                  new_description=action[1]["description"],
#                                  completed=action[1]["completed"],
#                                  priority=action[1]["priority"],
#                                  due_date=datetime.fromisoformat(action[1]["due_date"]) if action[1]["due_date"] else None,
#                                  tags=action[1]["tags"])
#     elif action[0] == "incomplete":
#         task_manager.update_task(action[1], completed=False)
#     save_tasks(task_manager.tasks)
#     console.print("[bold green]✅ Last action undone![/bold green]")

# # Main loop
# while True:
#     print_menu()
#     choice = Prompt.ask("[bold yellow]Select an option[/bold yellow]")

#     if choice == "1":
#         add_task()
#     elif choice == "2":
#         list_tasks()
#     elif choice == "3":
#         edit_task()
#     elif choice == "4":
#         complete_task()
#     elif choice == "5":
#         delete_task()
#     elif choice == "6":
#         search_task()
#     elif choice == "7":
#         due_today_tasks()
#     elif choice == "8":
#         undo_last_action()
#     elif choice == "0":
#         console.print("[bold magenta]👋 Exiting... Bye![/bold magenta]")
#         break
#     else:
#         console.print("[bold red]Invalid option![/bold red] Try again.")






# from todo_cli.core import TaskManager
# from todo_cli.storage import save_tasks, load_tasks
# from todo_cli.ui import display_tasks, console
# from datetime import datetime
# from rich.console import Console
# from rich.table import Table
# from rich.panel import Panel
# from rich.align import Align
# import os

# task_manager = TaskManager()
# task_manager.tasks = load_tasks()

# # History for undo functionality
# history = []

# def print_menu():
#     console.clear()
#     # Centered heading
#     heading = Align.center("[bold black]📝 TODO LIST MENU 📝[/bold black]")
#     console.print(Panel(heading, style="bold white on cyan", padding=(1,4)))

#     # Menu options table
#     menu_table = Table.grid(padding=1)
#     menu_table.add_column(justify="left")
#     menu_table.add_row("[bold green]1[/bold green] ➤ Add Task")
#     menu_table.add_row("[bold green]2[/bold green] ➤ List Tasks")
#     menu_table.add_row("[bold green]3[/bold green] ➤ Edit Task")
#     menu_table.add_row("[bold green]4[/bold green] ➤ Complete Task")
#     menu_table.add_row("[bold green]5[/bold green] ➤ Delete Task")
#     menu_table.add_row("[bold green]6[/bold green] ➤ Search Task")
#     menu_table.add_row("[bold green]7[/bold green] ➤ Show Due Today Tasks")
#     menu_table.add_row("[bold green]8[/bold green] ➤ Undo Last Action")
#     menu_table.add_row("[bold green]0[/bold green] ➤ Exit")

#     console.print(Panel(menu_table, border_style="bright_magenta"))

# def add_task_interactive():
#     description = console.input("Enter description: ")
#     priority_input = console.input("Enter priority (1-high, leave blank for none): ")
#     priority = int(priority_input) if priority_input.isdigit() else None
#     due_date_input = console.input("Enter due date (YYYY-MM-DD, leave blank for none): ")
#     due_date = None
#     if due_date_input:
#         try:
#             due_date = datetime.strptime(due_date_input, "%Y-%m-%d")
#         except ValueError:
#             console.print("[bold red]Invalid date format. Use YYYY-MM-DD.[/bold red]")
#             return
#     tags_input = console.input("Enter tags separated by commas (or leave blank): ")
#     tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []
    
#     task = task_manager.add_task(description, priority=priority, due_date=due_date, tags=tags)
#     history.append(("add", task))
#     save_tasks(task_manager.tasks)
#     console.print("[bold green]✅ Task added![/bold green]")

# def list_tasks_interactive():
#     display_tasks(task_manager.get_all_tasks())

# def edit_task_interactive():
#     task_id = console.input("Enter task ID to edit: ")
#     task = task_manager.get_task_by_id(task_id)
#     if not task:
#         console.print("[bold red]Task not found.[/bold red]")
#         return
#     description = console.input(f"New description (leave blank to keep '{task.description}'): ") or task.description
#     priority_input = console.input(f"New priority (leave blank to keep {task.priority}): ")
#     priority = int(priority_input) if priority_input.isdigit() else task.priority
#     due_date_input = console.input(f"New due date (YYYY-MM-DD, leave blank to keep {task.due_date}): ")
#     due_date = task.due_date
#     if due_date_input:
#         try:
#             due_date = datetime.strptime(due_date_input, "%Y-%m-%d")
#         except ValueError:
#             console.print("[bold red]Invalid date format. Keeping old date.[/bold red]")
#     tags_input = console.input(f"New tags (comma-separated, leave blank to keep {task.tags}): ")
#     tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else task.tags
    
#     old_task = task_manager.update_task(task_id, new_description=task.description, completed=task.completed,
#                                         priority=task.priority, due_date=task.due_date, tags=task.tags)
#     task_manager.update_task(task_id, new_description=description, priority=priority, due_date=due_date, tags=tags)
#     history.append(("edit", old_task))
#     save_tasks(task_manager.tasks)
#     console.print("[bold green]✅ Task updated![/bold green]")

# def complete_task_interactive():
#     task_id = console.input("Enter task ID to complete: ")
#     task = task_manager.update_task(task_id, completed=True)
#     if task:
#         history.append(("complete", task))
#         save_tasks(task_manager.tasks)
#         console.print("[bold green]✅ Task marked as completed![/bold green]")
#     else:
#         console.print("[bold red]Task not found.[/bold red]")

# def delete_task_interactive():
#     task_id = console.input("Enter task ID to delete: ")
#     task = task_manager.get_task_by_id(task_id)
#     if task:
#         task_manager.delete_task(task_id)
#         history.append(("delete", task))
#         save_tasks(task_manager.tasks)
#         console.print("[bold green]🗑️ Task deleted![/bold green]")
#     else:
#         console.print("[bold red]Task not found.[/bold red]")

# def search_task_interactive():
#     keyword = console.input("Enter search keyword: ")
#     results = task_manager.search_tasks(keyword)
#     display_tasks(results)

# def due_today_tasks_interactive():
#     today = datetime.today().date()
#     results = [task for task in task_manager.get_all_tasks() if task.due_date and task.due_date.date() == today]
#     display_tasks(results)

# def undo_last_action():
#     if not history:
#         console.print("[bold yellow]Nothing to undo.[/bold yellow]")
#         return
#     action, task = history.pop()
#     if action == "add":
#         task_manager.delete_task(task.id)
#     elif action == "delete":
#         task_manager.tasks.append(task)
#     elif action in ("edit", "complete"):
#         task_manager.update_task(task.id, new_description=task.description, completed=task.completed,
#                                  priority=task.priority, due_date=task.due_date, tags=task.tags)
#     save_tasks(task_manager.tasks)
#     console.print("[bold yellow]⏪ Last action undone![/bold yellow]")

# # Main loop
# while True:
#     print_menu()
#     choice = console.input("Select an option: ")

#     if choice == "1":
#         add_task_interactive()
#     elif choice == "2":
#         list_tasks_interactive()
#     elif choice == "3":
#         edit_task_interactive()
#     elif choice == "4":
#         complete_task_interactive()
#     elif choice == "5":
#         delete_task_interactive()
#     elif choice == "6":
#         search_task_interactive()
#     elif choice == "7":
#         due_today_tasks_interactive()
#     elif choice == "8":
#         undo_last_action()
#     elif choice == "0":
#         console.print("[bold cyan]Exiting... 👋[/bold cyan]")
#         break
#     else:
#         console.print("[bold red]Invalid option. Try again.[/bold red]")







from todo_cli.core import TaskManager
from todo_cli.storage import save_tasks, load_tasks
from todo_cli.ui import display_tasks, console
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
import os

task_manager = TaskManager()
task_manager.tasks = load_tasks()

# History for undo functionality
history = []

def print_menu():
    console.clear()
    # Centered heading
    heading = Align.center("[bold black]📝 TODO LIST MENU 📝[/bold black]")
    console.print(Panel(heading, style="bold white on cyan", padding=(1,4)))

    # Menu options table
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

def edit_task_interactive():
    task_id = console.input("Enter task ID to edit: ")
    task = task_manager.get_task_by_id(task_id)
    if not task:
        console.print("[bold red]Task not found.[/bold red]")
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
    
    old_task = task_manager.update_task(task_id, new_description=task.description, completed=task.completed,
                                        priority=task.priority, due_date=task.due_date, tags=task.tags)
    task_manager.update_task(task_id, new_description=description, priority=priority, due_date=due_date, tags=tags)
    history.append(("edit", old_task))
    save_tasks(task_manager.tasks)
    console.print("[bold green]✅ Task updated![/bold green]")

def complete_task_interactive():
    task_id = console.input("Enter task ID to complete: ")
    task = task_manager.update_task(task_id, completed=True)
    if task:
        history.append(("complete", task))
        save_tasks(task_manager.tasks)
        console.print("[bold green]✅ Task marked as completed![/bold green]")
    else:
        console.print("[bold red]Task not found.[/bold red]")

def delete_task_interactive():
    task_id = console.input("Enter task ID to delete: ")
    task = task_manager.get_task_by_id(task_id)
    if task:
        task_manager.delete_task(task_id)
        history.append(("delete", task))
        save_tasks(task_manager.tasks)
        console.print("[bold green]🗑️ Task deleted![/bold green]")
    else:
        console.print("[bold red]Task not found.[/bold red]")

def search_task_interactive():
    keyword = console.input("Enter search keyword: ")
    results = task_manager.search_tasks(keyword)
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

# Main loop
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
