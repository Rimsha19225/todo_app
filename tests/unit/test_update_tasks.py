"""
Unit tests for updating tasks functionality in the In-Memory Python Console Todo Application.
"""

import pytest
from src.todo_app.services.task_service import TaskService


class TestUpdateTasks:
    """Test class for updating tasks functionality."""

    def setup_method(self):
        """Set up a fresh TaskService instance for each test."""
        self.task_service = TaskService()

    def test_update_task_title(self):
        """Test updating a task's title."""
        task = self.task_service.add_task("Old Title", "Description")

        updated_task = self.task_service.update_task(task.id, "New Title")

        assert updated_task is not None
        assert updated_task.title == "New Title"
        assert updated_task.description == "Description"  # Should remain unchanged
        assert updated_task.id == task.id  # Should remain unchanged

    def test_update_task_description(self):
        """Test updating a task's description."""
        task = self.task_service.add_task("Title", "Old Description")

        updated_task = self.task_service.update_task(task.id, None, "New Description")

        assert updated_task is not None
        assert updated_task.title == "Title"  # Should remain unchanged
        assert updated_task.description == "New Description"
        assert updated_task.id == task.id  # Should remain unchanged

    def test_update_task_both_title_and_description(self):
        """Test updating both title and description of a task."""
        task = self.task_service.add_task("Old Title", "Old Description")

        updated_task = self.task_service.update_task(task.id, "New Title", "New Description")

        assert updated_task is not None
        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"
        assert updated_task.id == task.id  # Should remain unchanged

    def test_update_task_with_none_values(self):
        """Test that passing None for title/description doesn't update those fields."""
        task = self.task_service.add_task("Title", "Description")

        # Update with None values (should not change anything)
        updated_task = self.task_service.update_task(task.id, None, None)

        assert updated_task is not None
        assert updated_task.title == "Title"  # Should remain unchanged
        assert updated_task.description == "Description"  # Should remain unchanged
        assert updated_task.id == task.id  # Should remain unchanged

    def test_update_nonexistent_task(self):
        """Test updating a task that doesn't exist."""
        result = self.task_service.update_task("999", "New Title")

        assert result is None

    def test_update_task_title_validation(self):
        """Test that updating a task with empty title raises ValueError."""
        task = self.task_service.add_task("Title", "Description")

        with pytest.raises(ValueError, match="Title must not be empty or null"):
            self.task_service.update_task(task.id, "")

        with pytest.raises(ValueError, match="Title must not be empty or null"):
            self.task_service.update_task(task.id, "   ")  # Only whitespace

    def test_update_task_preserves_completion_status(self):
        """Test that updating a task preserves its completion status."""
        task = self.task_service.add_task("Title", "Description")
        # Mark task as complete first
        self.task_service.mark_task_complete(task.id)

        # Update the task
        updated_task = self.task_service.update_task(task.id, "New Title")

        assert updated_task is not None
        assert updated_task.completed is True  # Should remain completed

    def test_update_task_with_empty_description(self):
        """Test updating a task with an empty description."""
        task = self.task_service.add_task("Title", "Old Description")

        updated_task = self.task_service.update_task(task.id, None, "")

        assert updated_task is not None
        assert updated_task.description == ""