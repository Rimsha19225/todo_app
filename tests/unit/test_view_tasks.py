"""
Unit tests for viewing tasks functionality in the In-Memory Python Console Todo Application.
"""

import pytest
from src.todo_app.services.task_service import TaskService


class TestViewTasks:
    """Test class for viewing tasks functionality."""

    def setup_method(self):
        """Set up a fresh TaskService instance for each test."""
        self.task_service = TaskService()

    def test_get_all_tasks_initially_empty(self):
        """Test that initially there are no tasks."""
        tasks = self.task_service.get_all_tasks()

        assert len(tasks) == 0

    def test_get_all_tasks_after_adding_one_task(self):
        """Test getting all tasks after adding one task."""
        task = self.task_service.add_task("Test Task", "Test Description")

        tasks = self.task_service.get_all_tasks()

        assert len(tasks) == 1
        assert tasks[0].id == task.id
        assert tasks[0].title == "Test Task"
        assert tasks[0].description == "Test Description"
        assert tasks[0].completed is False

    def test_get_all_tasks_after_adding_multiple_tasks(self):
        """Test getting all tasks after adding multiple tasks."""
        task1 = self.task_service.add_task("Task 1", "Description 1")
        task2 = self.task_service.add_task("Task 2", "Description 2")
        task3 = self.task_service.add_task("Task 3", "Description 3")

        tasks = self.task_service.get_all_tasks()

        assert len(tasks) == 3
        assert tasks[0].id == task1.id
        assert tasks[1].id == task2.id
        assert tasks[2].id == task3.id

    def test_get_all_tasks_returns_copy_of_internal_list(self):
        """Test that get_all_tasks returns a copy, not the internal list."""
        self.task_service.add_task("Test Task", "Test Description")

        tasks = self.task_service.get_all_tasks()
        original_length = len(tasks)

        # Modify the returned list
        tasks.append("dummy")

        # Internal list should not be affected
        internal_tasks = self.task_service.get_all_tasks()
        assert len(internal_tasks) == original_length
        assert len(tasks) == original_length + 1

    def test_tasks_not_modified_by_external_changes(self):
        """Test that external modifications don't affect internal task storage."""
        task = self.task_service.add_task("Test Task", "Test Description")

        # Get task and modify it externally
        tasks = self.task_service.get_all_tasks()
        external_task = tasks[0]
        external_task.title = "Modified Title"

        # Internal task should remain unchanged
        internal_tasks = self.task_service.get_all_tasks()
        assert internal_tasks[0].title == "Test Task"