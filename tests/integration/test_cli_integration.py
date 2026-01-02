"""
Integration tests for the CLI interface in the In-Memory Python Console Todo Application.
"""

import pytest
from unittest.mock import patch
from io import StringIO
from src.todo_app.services.task_service import TaskService
from src.todo_app.cli.menu import Menu


class TestCLIIntegration:
    """Integration tests for CLI interface functionality."""

    def setup_method(self):
        """Set up a fresh TaskService and Menu instance for each test."""
        self.task_service = TaskService()
        self.menu = Menu(self.task_service)

    def test_add_and_view_task_integration(self):
        """Test the integration of adding and viewing a task."""
        # Add a task
        task = self.task_service.add_task("Test Task", "Test Description")

        # Verify it can be retrieved
        retrieved_task = self.task_service.get_task_by_id(task.id)
        assert retrieved_task is not None
        assert retrieved_task.title == "Test Task"
        assert retrieved_task.description == "Test Description"

        # Verify it appears in the list of all tasks
        all_tasks = self.task_service.get_all_tasks()
        assert len(all_tasks) == 1
        assert all_tasks[0].id == task.id

    def test_add_update_delete_integration(self):
        """Test the integration of adding, updating, and deleting a task."""
        # Add a task
        task = self.task_service.add_task("Original Title", "Original Description")

        # Update the task
        updated_task = self.task_service.update_task(task.id, "Updated Title", "Updated Description")
        assert updated_task is not None
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Updated Description"

        # Delete the task
        success = self.task_service.delete_task(task.id)
        assert success is True

        # Verify the task is gone
        all_tasks = self.task_service.get_all_tasks()
        assert len(all_tasks) == 0

        retrieved_task = self.task_service.get_task_by_id(task.id)
        assert retrieved_task is None

    def test_completion_integration(self):
        """Test the integration of task completion functionality."""
        # Add a task
        task = self.task_service.add_task("Test Task", "Test Description")

        # Verify it starts as incomplete
        assert task.completed is False

        # Mark as complete
        completed_task = self.task_service.mark_task_complete(task.id)
        assert completed_task is not None
        assert completed_task.completed is True

        # Mark as incomplete again
        incomplete_task = self.task_service.mark_task_incomplete(task.id)
        assert incomplete_task is not None
        assert incomplete_task.completed is False

    def test_multiple_tasks_integration(self):
        """Test the integration with multiple tasks."""
        # Add multiple tasks
        task1 = self.task_service.add_task("Task 1", "Description 1")
        task2 = self.task_service.add_task("Task 2", "Description 2")
        task3 = self.task_service.add_task("Task 3", "Description 3")

        # Verify all tasks exist
        all_tasks = self.task_service.get_all_tasks()
        assert len(all_tasks) == 3

        # Update one task
        updated_task = self.task_service.update_task(task2.id, "Updated Task 2")
        assert updated_task is not None
        assert updated_task.title == "Updated Task 2"

        # Mark one as complete
        completed_task = self.task_service.mark_task_complete(task1.id)
        assert completed_task is not None
        assert completed_task.completed is True

        # Delete one task
        success = self.task_service.delete_task(task3.id)
        assert success is True

        # Verify the state: 2 tasks remain, with proper completion status
        final_tasks = self.task_service.get_all_tasks()
        assert len(final_tasks) == 2

        task_ids = [t.id for t in final_tasks]
        assert task1.id in task_ids
        assert task2.id in task_ids
        assert task3.id not in task_ids  # task3 was deleted