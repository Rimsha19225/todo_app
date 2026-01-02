"""
Unit tests for the enhanced features of the In-Memory Python Console Todo Application.
Tests for priority, due date, and recurring pattern functionality.
"""

import pytest
from src.todo_app.services.task_service import TaskService
from src.todo_app.models.task import Task


class TestEnhancedTaskFeatures:
    """Test class for enhanced task features (priority, due date, recurring pattern)."""

    def setup_method(self):
        """Set up a fresh TaskService instance for each test."""
        self.task_service = TaskService()

    def test_add_task_with_priority(self):
        """Test adding a task with priority level."""
        task = self.task_service.add_task("Test Task", "Test Description", "high")

        assert task.priority == "high"
        assert task.title == "Test Task"
        assert task.description == "Test Description"

    def test_add_task_with_due_date(self):
        """Test adding a task with due date."""
        task = self.task_service.add_task("Test Task", "Test Description", "medium", "2026-12-31")

        assert task.due_date == "2026-12-31"
        assert task.priority == "medium"

    def test_add_task_with_recurring_pattern(self):
        """Test adding a task with recurring pattern."""
        task = self.task_service.add_task("Test Task", "Test Description", "low", "2026-12-31", "weekly")

        assert task.recurring_pattern == "weekly"
        assert task.due_date == "2026-12-31"
        assert task.priority == "low"

    def test_priority_validation(self):
        """Test that priority values are validated correctly."""
        # Valid priorities should work
        task1 = self.task_service.add_task("Task 1", priority="high")
        task2 = self.task_service.add_task("Task 2", priority="medium")
        task3 = self.task_service.add_task("Task 3", priority="low")

        assert task1.priority == "high"
        assert task2.priority == "medium"
        assert task3.priority == "low"

        # Invalid priority should raise an error
        with pytest.raises(ValueError, match="Priority must be one of"):
            self.task_service.add_task("Invalid Task", priority="urgent")

    def test_recurring_pattern_validation(self):
        """Test that recurring pattern values are validated correctly."""
        # Valid patterns should work
        task1 = self.task_service.add_task("Task 1", recurring_pattern="daily")
        task2 = self.task_service.add_task("Task 2", recurring_pattern="weekly")
        task3 = self.task_service.add_task("Task 3", recurring_pattern="monthly")
        task4 = self.task_service.add_task("Task 4", recurring_pattern="none")

        assert task1.recurring_pattern == "daily"
        assert task2.recurring_pattern == "weekly"
        assert task3.recurring_pattern == "monthly"
        assert task4.recurring_pattern == "none"

        # Invalid pattern should raise an error
        with pytest.raises(ValueError, match="Recurring pattern must be one of"):
            self.task_service.add_task("Invalid Task", recurring_pattern="yearly")

    def test_due_date_validation(self):
        """Test that due date format is validated correctly."""
        # Valid date format should work
        task = self.task_service.add_task("Task", due_date="2026-12-31")
        assert task.due_date == "2026-12-31"

        # Invalid date format should raise an error
        with pytest.raises(ValueError, match="Due date must be in YYYY-MM-DD format"):
            self.task_service.add_task("Invalid Task", due_date="31-12-2026")

        # Invalid date should raise an error
        with pytest.raises(ValueError, match="Due date must be in YYYY-MM-DD format"):
            self.task_service.add_task("Invalid Task", due_date="2026-02-30")  # Feb 30 doesn't exist

    def test_update_task_priority(self):
        """Test updating task priority."""
        task = self.task_service.add_task("Test Task", priority="low")

        updated_task = self.task_service.update_task(task.id, priority="high")

        assert updated_task is not None
        assert updated_task.priority == "high"
        assert updated_task.title == "Test Task"

    def test_update_task_due_date(self):
        """Test updating task due date."""
        task = self.task_service.add_task("Test Task", due_date="2026-01-01")

        updated_task = self.task_service.update_task(task.id, due_date="2026-12-31")

        assert updated_task is not None
        assert updated_task.due_date == "2026-12-31"

    def test_update_task_recurring_pattern(self):
        """Test updating task recurring pattern."""
        task = self.task_service.add_task("Test Task", recurring_pattern="none")

        updated_task = self.task_service.update_task(task.id, recurring_pattern="daily")

        assert updated_task is not None
        assert updated_task.recurring_pattern == "daily"

    def test_update_task_all_fields(self):
        """Test updating all fields of a task."""
        task = self.task_service.add_task("Old Title", "Old Description", "low", "2026-01-01", "none")

        updated_task = self.task_service.update_task(
            task.id,
            title="New Title",
            description="New Description",
            priority="high",
            due_date="2026-12-31",
            recurring_pattern="weekly"
        )

        assert updated_task is not None
        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"
        assert updated_task.priority == "high"
        assert updated_task.due_date == "2026-12-31"
        assert updated_task.recurring_pattern == "weekly"

    def test_task_string_representation_with_new_fields(self):
        """Test that the task string representation includes new fields."""
        task = self.task_service.add_task("Test Task", "Description", "high", "2026-12-31", "weekly")

        task_str = str(task)
        assert "Test Task" in task_str
        assert "P:H" in task_str  # High priority should show as H
        assert "2026-12-31" in task_str
        assert "Rec: W" in task_str  # Weekly recurring should show as W (with space)

    def test_default_values(self):
        """Test that tasks have correct default values."""
        task = self.task_service.add_task("Test Task")

        assert task.priority == "medium"
        assert task.due_date is None
        assert task.recurring_pattern == "none"

    def test_get_all_tasks_includes_new_fields(self):
        """Test that get_all_tasks returns tasks with all new fields."""
        task = self.task_service.add_task("Test Task", "Description", "high", "2026-12-31", "daily")
        all_tasks = self.task_service.get_all_tasks()

        assert len(all_tasks) == 1
        retrieved_task = all_tasks[0]
        assert retrieved_task.title == "Test Task"
        assert retrieved_task.description == "Description"
        assert retrieved_task.priority == "high"
        assert retrieved_task.due_date == "2026-12-31"
        assert retrieved_task.recurring_pattern == "daily"
        # Verify it's a different object (copy)
        assert retrieved_task is not task

    def test_get_task_by_id_includes_new_fields(self):
        """Test that get_task_by_id returns tasks with all new fields."""
        task = self.task_service.add_task("Test Task", "Description", "low", "2026-06-15", "monthly")
        retrieved_task = self.task_service.get_task_by_id(task.id)

        assert retrieved_task is not None
        assert retrieved_task.title == "Test Task"
        assert retrieved_task.description == "Description"
        assert retrieved_task.priority == "low"
        assert retrieved_task.due_date == "2026-06-15"
        assert retrieved_task.recurring_pattern == "monthly"
        # Verify it's a different object (copy)
        assert retrieved_task is not task