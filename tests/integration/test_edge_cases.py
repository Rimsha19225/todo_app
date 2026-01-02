"""
Tests for edge cases and error handling from the specification in the In-Memory Python Console Todo Application.
"""

import pytest
from src.todo_app.services.task_service import TaskService


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def setup_method(self):
        """Set up a fresh TaskService instance for each test."""
        self.task_service = TaskService()

    def test_invalid_task_id_operations(self):
        """
        Edge Case: What happens when a user tries to perform an operation on a task ID that doesn't exist?
        """
        # Test getting non-existent task
        task = self.task_service.get_task_by_id("999")
        assert task is None

        # Test updating non-existent task
        result = self.task_service.update_task("999", "New Title")
        assert result is None

        # Test deleting non-existent task
        success = self.task_service.delete_task("999")
        assert success is False

        # Test marking complete non-existent task
        result = self.task_service.mark_task_complete("999")
        assert result is None

        # Test marking incomplete non-existent task
        result = self.task_service.mark_task_incomplete("999")
        assert result is None

    def test_empty_input_when_adding_task(self):
        """
        Edge Case: How does the system handle empty input when adding a task?
        """
        with pytest.raises(ValueError, match="Title must not be empty or null"):
            self.task_service.add_task("")

        with pytest.raises(ValueError, match="Title must not be empty or null"):
            self.task_service.add_task("   ")  # Only whitespace

    def test_very_long_titles_and_descriptions(self):
        """
        Edge Case: How does the system handle very long titles or descriptions?
        """
        long_title = "A" * 600  # Exceeds the 500 character limit mentioned in data model
        long_description = "B" * 2500  # Exceeds the 2000 character limit mentioned in data model

        # The system should reject these since they exceed the character limits
        with pytest.raises(ValueError, match="Title must not exceed 500 characters"):
            self.task_service.add_task(long_title, "valid description")

        # Test description limit as well
        with pytest.raises(ValueError, match="Description must not exceed 2000 characters"):
            self.task_service.add_task("valid title", long_description)

    def test_task_id_uniqueness(self):
        """
        Edge Case: Verify that task IDs are unique.
        """
        task1 = self.task_service.add_task("Task 1")
        task2 = self.task_service.add_task("Task 2")
        task3 = self.task_service.add_task("Task 3")

        # IDs should be unique
        ids = [task1.id, task2.id, task3.id]
        assert len(ids) == len(set(ids))  # All IDs should be unique

        # IDs should be sequential starting from 1
        assert ids == ["1", "2", "3"]

    def test_completion_status_transitions(self):
        """
        Edge Case: Test various completion status transitions.
        """
        task = self.task_service.add_task("Test Task")

        # Initially incomplete
        assert task.completed is False

        # Mark complete
        completed_task = self.task_service.mark_task_complete(task.id)
        assert completed_task.completed is True

        # Mark complete again (should remain complete)
        still_completed = self.task_service.mark_task_complete(task.id)
        assert still_completed.completed is True

        # Mark incomplete
        incomplete_task = self.task_service.mark_task_incomplete(task.id)
        assert incomplete_task.completed is False

        # Mark incomplete again (should remain incomplete)
        still_incomplete = self.task_service.mark_task_incomplete(task.id)
        assert still_incomplete.completed is False

    def test_empty_description_handling(self):
        """
        Edge Case: Test handling of empty descriptions.
        """
        task_with_empty_desc = self.task_service.add_task("Task with empty desc", "")
        task_without_desc_param = self.task_service.add_task("Task without desc param")

        assert task_with_empty_desc.description == ""
        assert task_without_desc_param.description == ""

    def test_special_characters_in_task_fields(self):
        """
        Edge Case: Test handling of special characters in task fields.
        """
        special_title = "Task with special chars: !@#$%^&*()"
        special_description = "Description with special chars: []{}|;:,.<>?~`"

        task = self.task_service.add_task(special_title, special_description)

        assert task.title == special_title
        assert task.description == special_description

    def test_unicode_characters_in_task_fields(self):
        """
        Edge Case: Test handling of Unicode characters in task fields.
        """
        unicode_title = "Task with unicode: café 🌟"
        unicode_description = "Description with unicode: résumé 📝"

        task = self.task_service.add_task(unicode_title, unicode_description)

        assert task.title == unicode_title
        assert task.description == unicode_description


class TestErrorHandling:
    """Tests for error handling scenarios."""

    def setup_method(self):
        """Set up a fresh TaskService instance for each test."""
        self.task_service = TaskService()

    def test_add_task_with_invalid_title(self):
        """Test error handling when adding a task with invalid title."""
        with pytest.raises(ValueError, match="Title must not be empty or null"):
            self.task_service.add_task("")

        with pytest.raises(ValueError, match="Title must not be empty or null"):
            self.task_service.add_task("   ")

    def test_update_task_with_invalid_title(self):
        """Test error handling when updating a task with invalid title."""
        task = self.task_service.add_task("Valid Task")

        with pytest.raises(ValueError, match="Title must not be empty or null"):
            self.task_service.update_task(task.id, "")

        with pytest.raises(ValueError, match="Title must not be empty or null"):
            self.task_service.update_task(task.id, "   ")

    def test_add_task_with_none_title(self):
        """Test error handling when adding a task with None title."""
        with pytest.raises(ValueError, match="Title must not be empty or null"):
            self.task_service.add_task(None)

    def test_get_task_by_none_id(self):
        """Test error handling when getting a task with None ID."""
        # This should return None rather than raise an error
        result = self.task_service.get_task_by_id(None)
        assert result is None

    def test_delete_task_by_none_id(self):
        """Test error handling when deleting a task with None ID."""
        # This should return False rather than raise an error
        success = self.task_service.delete_task(None)
        assert success is False