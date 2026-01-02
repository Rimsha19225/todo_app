"""
Unit tests for the TaskService class in the In-Memory Python Console Todo Application.
"""

import pytest
from src.todo_app.services.task_service import TaskService
from src.todo_app.models.task import Task


class TestTaskService:
    """Test class for TaskService functionality."""

    def setup_method(self):
        """Set up a fresh TaskService instance for each test."""
        self.task_service = TaskService()

    def test_add_task_with_title_and_description(self):
        """Test adding a task with both title and description."""
        title = "Test Task"
        description = "Test Description"

        task = self.task_service.add_task(title, description)

        assert task.title == title
        assert task.description == description
        assert task.completed is False
        assert task.id == "1"  # First task should get ID "1"

    def test_add_task_with_title_only(self):
        """Test adding a task with only a title."""
        title = "Test Task"

        task = self.task_service.add_task(title)

        assert task.title == title
        assert task.description == ""
        assert task.completed is False
        assert task.id == "1"  # First task should get ID "1"

    def test_add_task_with_empty_description(self):
        """Test adding a task with an empty description."""
        title = "Test Task"
        description = ""

        task = self.task_service.add_task(title, description)

        assert task.title == title
        assert task.description == ""
        assert task.completed is False
        assert task.id == "1"  # First task should get ID "1"

    def test_add_task_title_validation(self):
        """Test that adding a task with empty title raises ValueError."""
        with pytest.raises(ValueError, match="Title must not be empty or null"):
            self.task_service.add_task("")

        with pytest.raises(ValueError, match="Title must not be empty or null"):
            self.task_service.add_task("   ")  # Only whitespace

    def test_get_all_tasks_initially_empty(self):
        """Test that initially there are no tasks."""
        tasks = self.task_service.get_all_tasks()

        assert len(tasks) == 0

    def test_get_all_tasks_after_adding(self):
        """Test getting all tasks after adding some."""
        self.task_service.add_task("Task 1", "Description 1")
        self.task_service.add_task("Task 2", "Description 2")

        tasks = self.task_service.get_all_tasks()

        assert len(tasks) == 2
        assert tasks[0].title == "Task 1"
        assert tasks[1].title == "Task 2"

    def test_get_task_by_id_existing(self):
        """Test getting a task by its ID when it exists."""
        task = self.task_service.add_task("Test Task", "Description")
        task_id = task.id

        retrieved_task = self.task_service.get_task_by_id(task_id)

        assert retrieved_task is not None
        assert retrieved_task.id == task_id
        assert retrieved_task.title == "Test Task"
        assert retrieved_task.description == "Description"

    def test_get_task_by_id_nonexistent(self):
        """Test getting a task by its ID when it doesn't exist."""
        retrieved_task = self.task_service.get_task_by_id("999")

        assert retrieved_task is None

    def test_add_multiple_tasks_incremental_ids(self):
        """Test that multiple tasks get incremental IDs."""
        task1 = self.task_service.add_task("Task 1")
        task2 = self.task_service.add_task("Task 2")
        task3 = self.task_service.add_task("Task 3")

        assert task1.id == "1"
        assert task2.id == "2"
        assert task3.id == "3"

    def test_task_attributes_after_creation(self):
        """Test that task attributes are correctly set after creation."""
        title = "My Task"
        description = "My Description"

        task = self.task_service.add_task(title, description)

        assert isinstance(task, Task)
        assert task.id.isdigit()  # ID should be numeric string
        assert task.title == title
        assert task.description == description
        assert task.completed is False