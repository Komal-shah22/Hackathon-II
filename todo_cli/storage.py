import json
from typing import List
from todo_cli.models import Task
import os
import tempfile

TASKS_FILE = "tasks.json"

def load_tasks() -> List[Task]:
    """
    Loads tasks from the JSON storage file.
    If the file does not exist, returns an empty list.
    """
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        tasks_data = json.load(f)
    return [Task.from_dict(data) for data in tasks_data]

def save_tasks(tasks: List[Task]):
    """
    Saves tasks to the JSON storage file using atomic write.
    """
    tasks_data = [task.to_dict() for task in tasks]
    
    # Use a temporary file for atomic write
    with tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8") as temp_file:
        json.dump(tasks_data, temp_file, indent=4)
    
    # Atomically replace the old file with the new one
    os.replace(temp_file.name, TASKS_FILE)