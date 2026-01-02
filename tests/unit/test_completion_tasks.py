"""
Unit tests for task completion functionality in the In-Memory Python Console Todo Application.
"""

import pytest
from src.todo_app.services.task_service import TaskService


class TestCompletionTasks:
    """Test class for task completion functionality."""

    def setup_method(self):
        """Set up a fresh TaskService instance for each test."""
        self.task_service = TaskService()

    def test_mark_task_complete(self):
        """Test marking a task as complete."""
        task = self.task_service.add_task("Test Task", "Description")

        updated_task = self.task_service.mark_task_complete(task.id)

        assert updated_task is not None
        assert updated_task.completed is True
        assert updated_task.title == "Test Task"
        assert updated_task.description == "Description"

    def test_mark_task_incomplete(self):
        """Test marking a task as incomplete."""
        task = self.task_service.add_task("Test Task", "Description")
        # First mark it complete
        self.task_service.mark_task_complete(task.id)

        updated_task = self.task_service.mark_task_incomplete(task.id)

        assert updated_task is not None
        assert updated_task.completed is False
        assert updated_task.title == "Test Task"
        assert updated_task.description == "Description"

    def test_mark_nonexistent_task_complete(self):
        """Test marking a non-existent task as complete."""
        result = self.task_service.mark_task_complete("999")

        assert result is None

    def test_mark_nonexistent_task_incomplete(self):
        """Test marking a non-existent task as incomplete."""
        result = self.task_service.mark_task_incomplete("999")

        assert result is None

    def test_task_initially_incomplete(self):
        """Test that a newly created task is initially incomplete."""
        task = self.task_service.add_task("Test Task", "Description")

        assert task.completed is False

    def test_mark_task_complete_then_incomplete(self):
        """Test marking a task complete then incomplete."""
        task = self.task_service.add_task("Test Task", "Description")

        # Mark complete
        updated_task = self.task_service.mark_task_complete(task.id)
        assert updated_task.completed is True

        # Mark incomplete
        updated_task = self.task_service.mark_task_incomplete(task.id)
        assert updated_task.completed is False

    def test_mark_task_incomplete_then_complete(self):
        """Test marking a task incomplete then complete."""
        task = self.task_service.add_task("Test Task", "Description")

        # Mark incomplete (though it's already incomplete by default)
        updated_task = self.task_service.mark_task_incomplete(task.id)
        assert updated_task.completed is False

        # Mark complete
        updated_task = self.task_service.mark_task_complete(task.id)
        assert updated_task.completed is True

    def test_completion_status_persists_after_get_all_tasks(self):
        """Test that completion status is preserved when retrieving all tasks."""
        task = self.task_service.add_task("Test Task", "Description")

        # Mark as complete
        self.task_service.mark_task_complete(task.id)

        # Get all tasks and verify completion status
        all_tasks = self.task_service.get_all_tasks()
        assert len(all_tasks) == 1
        assert all_tasks[0].completed is True

    def test_completion_status_persists_after_other_operations(self):
        """Test that completion status is preserved after other operations."""
        task1 = self.task_service.add_task("Task 1", "Description 1")
        task2 = self.task_service.add_task("Task 2", "Description 2")

        # Mark task1 as complete
        self.task_service.mark_task_complete(task1.id)

        # Perform other operations
        self.task_service.update_task(task2.id, "Updated Task 2")

        # Verify task1 is still complete
        retrieved_task1 = self.task_service.get_task_by_id(task1.id)
        assert retrieved_task1.completed is True