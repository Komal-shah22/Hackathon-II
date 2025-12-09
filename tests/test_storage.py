import pytest
import os
import json
from todo_cli import storage
from todo_cli.models import Task

@pytest.fixture
def tasks_file(tmp_path):
    """Fixture to provide a temporary tasks.json file."""
    # Ensure the TASKS_FILE constant points to the temporary path
    original_tasks_file = storage.TASKS_FILE
    storage.TASKS_FILE = tmp_path / "tasks.json"
    yield storage.TASKS_FILE
    # Restore original TASKS_FILE path
    storage.TASKS_FILE = original_tasks_file

@pytest.fixture
def sample_tasks():
    """Fixture to provide a list of sample Task objects."""
    task1 = Task(description="Buy groceries", completed=False)
    task2 = Task(description="Read a book", completed=True)
    return [task1, task2]

def test_save_tasks_creates_file(tasks_file, sample_tasks):
    """Test that save_tasks creates the JSON file."""
    storage.save_tasks(sample_tasks)
    assert os.path.exists(tasks_file)

def test_save_tasks_correct_content(tasks_file, sample_tasks):
    """Test that save_tasks writes the correct content."""
    storage.save_tasks(sample_tasks)
    with open(tasks_file, "r") as f:
        data = json.load(f)
    assert len(data) == len(sample_tasks)
    assert data[0]["description"] == sample_tasks[0].description
    assert data[1]["completed"] == sample_tasks[1].completed

def test_load_tasks_empty_file(tasks_file):
    """Test loading tasks from a non-existent file returns an empty list."""
    # Ensure file does not exist
    if os.path.exists(tasks_file):
        os.remove(tasks_file)
    
    loaded_tasks = storage.load_tasks()
    assert loaded_tasks == []

def test_load_tasks_existing_file(tasks_file, sample_tasks):
    """Test loading tasks from an existing file."""
    # Manually create the file with sample data
    tasks_data = [task.to_dict() for task in sample_tasks]
    with open(tasks_file, "w") as f:
        json.dump(tasks_data, f)
    
    loaded_tasks = storage.load_tasks()
    assert len(loaded_tasks) == len(sample_tasks)
    assert loaded_tasks[0].description == sample_tasks[0].description
    assert loaded_tasks[1].completed == sample_tasks[1].completed
    assert isinstance(loaded_tasks[0], Task)

def test_atomic_write(tasks_file, sample_tasks):
    """Test that save_tasks atomically overwrites a corrupt file."""
    # 1. Create a corrupt version of the tasks file
    with open(tasks_file, "w") as f:
        f.write("this is corrupt json")
    
    # 2. Call save_tasks, which should atomically replace the corrupt file
    storage.save_tasks(sample_tasks)
    
    # 3. Verify the file now contains the correct, uncorrupted data
    with open(tasks_file, "r") as f:
        data = json.load(f)
    
    assert len(data) == len(sample_tasks)
    assert data[0]["description"] == sample_tasks[0].description
    assert data[1]["id"] == sample_tasks[1].id
