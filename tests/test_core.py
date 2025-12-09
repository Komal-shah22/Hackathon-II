import pytest
from datetime import datetime
from todo_cli.core import TaskManager
from todo_cli.models import Task

@pytest.fixture
def task_manager():
    """Fixture to provide a clean TaskManager for each test."""
    manager = TaskManager()
    # Ensure tasks list is empty for a clean state
    manager.tasks = []
    return manager

def test_add_task(task_manager):
    """Test adding a new task."""
    task = task_manager.add_task("Buy groceries")
    assert len(task_manager.tasks) == 1
    assert task.description == "Buy groceries"
    assert not task.completed
    assert task.id is not None

def test_add_task_with_metadata(task_manager):
    """Test adding a new task with priority, due date, and tags."""
    due_date = datetime(2025, 12, 31)
    task = task_manager.add_task("Plan party", priority=1, due_date=due_date, tags=["social", "fun"])
    assert len(task_manager.tasks) == 1
    assert task.description == "Plan party"
    assert task.priority == 1
    assert task.due_date == due_date
    assert task.tags == ["social", "fun"]

def test_get_all_tasks(task_manager):
    """Test retrieving all tasks."""
    task_manager.add_task("Task 1")
    task_manager.add_task("Task 2")
    tasks = task_manager.get_all_tasks()
    assert len(tasks) == 2
    assert tasks[0].description == "Task 1"
    assert tasks[1].description == "Task 2"

def test_get_task_by_id(task_manager):
    """Test retrieving a task by its ID."""
    task1 = task_manager.add_task("Unique task")
    retrieved_task = task_manager.get_task_by_id(task1.id)
    assert retrieved_task == task1

def test_get_task_by_id_not_found(task_manager):
    """Test retrieving a non-existent task by ID."""
    retrieved_task = task_manager.get_task_by_id("non-existent-id")
    assert retrieved_task is None

def test_update_task_description(task_manager):
    """Test updating a task's description."""
    task = task_manager.add_task("Old description")
    updated_task = task_manager.update_task(task.id, new_description="New description")
    assert updated_task is not None
    assert updated_task.description == "New description"
    assert task.description == "New description" # Check in-memory object

def test_update_task_completion(task_manager):
    """Test updating a task's completion status."""
    task = task_manager.add_task("Uncompleted task")
    updated_task = task_manager.update_task(task.id, completed=True)
    assert updated_task is not None
    assert updated_task.completed is True
    assert task.completed is True

def test_update_task_priority(task_manager):
    """Test updating a task's priority."""
    task = task_manager.add_task("Task with no priority")
    updated_task = task_manager.update_task(task.id, priority=3)
    assert updated_task is not None
    assert updated_task.priority == 3
    assert task.priority == 3

def test_update_task_due_date(task_manager):
    """Test updating a task's due date."""
    task = task_manager.add_task("Task with no due date")
    new_due_date = datetime(2026, 1, 1)
    updated_task = task_manager.update_task(task.id, due_date=new_due_date)
    assert updated_task is not None
    assert updated_task.due_date == new_due_date
    assert task.due_date == new_due_date

def test_update_task_tags(task_manager):
    """Test updating a task's tags."""
    task = task_manager.add_task("Task with old tags", tags=["old"])
    new_tags = ["new", "fresh"]
    updated_task = task_manager.update_task(task.id, tags=new_tags)
    assert updated_task is not None
    assert updated_task.tags == new_tags
    assert task.tags == new_tags

def test_update_task_not_found(task_manager):
    """Test updating a non-existent task."""
    updated_task = task_manager.update_task("non-existent-id", new_description="Attempt update")
    assert updated_task is None

def test_delete_task(task_manager):
    """Test deleting an existing task."""
    task = task_manager.add_task("Task to delete")
    assert task_manager.delete_task(task.id) is True
    assert len(task_manager.tasks) == 0

def test_delete_task_not_found(task_manager):
    """Test deleting a non-existent task."""
    task_manager.add_task("Keep me")
    assert task_manager.delete_task("non-existent-id") is False
    assert len(task_manager.tasks) == 1

def test_search_tasks_by_keyword(task_manager):
    """Test searching tasks by a keyword in description."""
    task_manager.add_task("Buy groceries")
    task_manager.add_task("Read a book")
    task_manager.add_task("Do laundry")
    
    results = task_manager.search_tasks("buy")
    assert len(results) == 1
    assert results[0].description == "Buy groceries"

    results = task_manager.search_tasks("task")
    assert len(results) == 0 # "Task" is in add_task param, not description here

def test_search_tasks_case_insensitive(task_manager):
    """Test case-insensitive search."""
    task_manager.add_task("Walk the DOG")
    results = task_manager.search_tasks("dog")
    assert len(results) == 1
    assert results[0].description == "Walk the DOG"

def test_search_tasks_no_match(task_manager):
    """Test search with no matching tasks."""
    task_manager.add_task("Task one")
    results = task_manager.search_tasks("xyz")
    assert len(results) == 0

def test_get_all_tasks_filter_by_tag(task_manager):
    """Test filtering tasks by tag."""
    task_manager.add_task("Work on project", tags=["work", "urgent"])
    task_manager.add_task("Buy milk", tags=["home"])
    task_manager.add_task("Review code", tags=["work"])

    filtered = task_manager.get_all_tasks(tag="work")
    assert len(filtered) == 2
    assert all("work" in t.tags for t in filtered)

    filtered = task_manager.get_all_tasks(tag="urgent")
    assert len(filtered) == 1
    assert "Work on project" in [t.description for t in filtered]

def test_get_all_tasks_filter_by_priority(task_manager):
    """Test filtering tasks by priority."""
    task_manager.add_task("High prio", priority=1)
    task_manager.add_task("Low prio", priority=5)
    task_manager.add_task("Another high prio", priority=1)

    filtered = task_manager.get_all_tasks(priority=1)
    assert len(filtered) == 2
    assert all(t.priority == 1 for t in filtered)

def test_get_all_tasks_filter_by_completed_status(task_manager):
    """Test filtering tasks by completion status."""
    task_manager.add_task("Done task", completed=True)
    task_manager.add_task("Pending task", completed=False)
    task_manager.add_task("Another done task", completed=True)

    filtered = task_manager.get_all_tasks(completed=True)
    assert len(filtered) == 2
    assert all(t.completed is True for t in filtered)

    filtered = task_manager.get_all_tasks(completed=False)
    assert len(filtered) == 1
    assert all(t.completed is False for t in filtered)

def test_get_all_tasks_multiple_filters(task_manager):
    """Test filtering tasks by multiple criteria."""
    task_manager.add_task("Urgent work", priority=1, tags=["work"], completed=False)
    task_manager.add_task("Casual reading", priority=5, tags=["leisure"], completed=False)
    task_manager.add_task("Done work", priority=1, tags=["work"], completed=True)

    filtered = task_manager.get_all_tasks(tag="work", priority=1, completed=False)
    assert len(filtered) == 1
    assert filtered[0].description == "Urgent work"

    filtered = task_manager.get_all_tasks(tag="work", completed=True)
    assert len(filtered) == 1
    assert filtered[0].description == "Done work"
