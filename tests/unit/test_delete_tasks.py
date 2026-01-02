"""
Unit tests for deleting tasks functionality in the In-Memory Python Console Todo Application.
"""

import pytest
from src.todo_app.services.task_service import TaskService


class TestDeleteTasks:
    """Test class for deleting tasks functionality."""

    def setup_method(self):
        """Set up a fresh TaskService instance for each test."""
        self.task_service = TaskService()

    def test_delete_existing_task(self):
        """Test deleting an existing task."""
        task = self.task_service.add_task("Test Task", "Description")

        success = self.task_service.delete_task(task.id)

        assert success is True
        # Verify the task is no longer in the list
        tasks = self.task_service.get_all_tasks()
        assert len(tasks) == 0

    def test_delete_nonexistent_task(self):
        """Test deleting a task that doesn't exist."""
        success = self.task_service.delete_task("999")

        assert success is False

    def test_delete_task_removes_only_correct_task(self):
        """Test that deleting a task only removes the specific task."""
        task1 = self.task_service.add_task("Task 1", "Description 1")
        task2 = self.task_service.add_task("Task 2", "Description 2")
        task3 = self.task_service.add_task("Task 3", "Description 3")

        success = self.task_service.delete_task(task2.id)

        assert success is True
        remaining_tasks = self.task_service.get_all_tasks()
        assert len(remaining_tasks) == 2
        # Verify task1 and task3 still exist
        assert remaining_tasks[0].id == task1.id
        assert remaining_tasks[1].id == task3.id
        # Verify task2 is gone
        assert task2.id not in [t.id for t in remaining_tasks]

    def test_delete_task_then_try_to_get_it(self):
        """Test that a deleted task can't be retrieved."""
        task = self.task_service.add_task("Test Task", "Description")

        # Delete the task
        self.task_service.delete_task(task.id)

        # Try to get the deleted task
        result = self.task_service.get_task_by_id(task.id)
        assert result is None

    def test_delete_task_then_try_to_update_it(self):
        """Test that a deleted task can't be updated."""
        task = self.task_service.add_task("Test Task", "Description")

        # Delete the task
        self.task_service.delete_task(task.id)

        # Try to update the deleted task
        result = self.task_service.update_task(task.id, "New Title")
        assert result is None

    def test_delete_all_tasks(self):
        """Test deleting all tasks one by one."""
        task1 = self.task_service.add_task("Task 1", "Description 1")
        task2 = self.task_service.add_task("Task 2", "Description 2")

        # Delete all tasks
        success1 = self.task_service.delete_task(task1.id)
        success2 = self.task_service.delete_task(task2.id)

        assert success1 is True
        assert success2 is True
        assert len(self.task_service.get_all_tasks()) == 0

    def test_delete_task_preserves_other_task_ids(self):
        """Test that deleting a task doesn't affect other task IDs."""
        task1 = self.task_service.add_task("Task 1", "Description 1")
        task2 = self.task_service.add_task("Task 2", "Description 2")
        task3 = self.task_service.add_task("Task 3", "Description 3")

        # Delete middle task
        self.task_service.delete_task(task2.id)

        # Verify remaining tasks still have their original IDs
        remaining_tasks = self.task_service.get_all_tasks()
        remaining_ids = [t.id for t in remaining_tasks]
        assert task1.id in remaining_ids
        assert task3.id in remaining_ids
        assert task2.id not in remaining_ids