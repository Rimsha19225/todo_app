"""
Unit tests for the recurring tasks and due date reminder features of the In-Memory Python Console Todo Application.
"""

import pytest
from datetime import datetime, timedelta
from src.todo_app.services.task_service import TaskService
from src.todo_app.models.task import Task


class TestRecurringTasks:
    """Test class for recurring tasks functionality."""

    def setup_method(self):
        """Set up a fresh TaskService instance for each test."""
        self.task_service = TaskService()

    def test_calculate_next_due_date_daily(self):
        """Test calculating next due date for daily recurring tasks."""
        current_date = "2026-01-15"
        next_date = self.task_service._calculate_next_due_date(current_date, "daily")
        assert next_date == "2026-01-16"

    def test_calculate_next_due_date_weekly(self):
        """Test calculating next due date for weekly recurring tasks."""
        current_date = "2026-01-15"
        next_date = self.task_service._calculate_next_due_date(current_date, "weekly")
        assert next_date == "2026-01-22"

    def test_calculate_next_due_date_monthly_same_month(self):
        """Test calculating next due date for monthly recurring tasks within same month range."""
        current_date = "2026-01-15"
        next_date = self.task_service._calculate_next_due_date(current_date, "monthly")
        assert next_date == "2026-02-15"

    def test_calculate_next_due_date_monthly_year_transition(self):
        """Test calculating next due date for monthly recurring tasks across year boundary."""
        current_date = "2026-12-15"
        next_date = self.task_service._calculate_next_due_date(current_date, "monthly")
        assert next_date == "2027-01-15"

    def test_calculate_next_due_date_invalid_pattern(self):
        """Test calculating next due date for invalid recurring pattern."""
        current_date = "2026-01-15"
        next_date = self.task_service._calculate_next_due_date(current_date, "invalid")
        assert next_date is None

    def test_calculate_next_due_date_none_input(self):
        """Test calculating next due date for None input."""
        next_date = self.task_service._calculate_next_due_date(None, "daily")
        assert next_date is None

    def test_calculate_next_due_date_empty_input(self):
        """Test calculating next due date for empty input."""
        next_date = self.task_service._calculate_next_due_date("", "daily")
        assert next_date is None

    def test_mark_task_complete_creates_new_recurring_task_daily(self):
        """Test that marking a daily recurring task as complete creates a new instance."""
        original_task = self.task_service.add_task(
            "Daily meeting", "Team standup", "medium", "2026-01-15", "daily", "work"
        )

        # Mark the task as complete
        completed_task = self.task_service.mark_task_complete(original_task.id)

        # Verify the original task is marked as complete
        assert completed_task.completed is True

        # Get all tasks to check if a new one was created
        all_tasks = self.task_service.get_all_tasks()
        incomplete_tasks = [task for task in all_tasks if not task.completed]

        # Should have 1 incomplete task (the new recurring instance)
        assert len(incomplete_tasks) == 1
        new_task = incomplete_tasks[0]

        # Verify the new task has the same properties as the original
        assert new_task.title == original_task.title
        assert new_task.description == original_task.description
        assert new_task.priority == original_task.priority
        assert new_task.category == original_task.category
        assert new_task.recurring_pattern == original_task.recurring_pattern

        # Verify the due date is updated for the next day
        assert new_task.due_date == "2026-01-16"

    def test_mark_task_complete_creates_new_recurring_task_weekly(self):
        """Test that marking a weekly recurring task as complete creates a new instance."""
        original_task = self.task_service.add_task(
            "Weekly report", "Write weekly summary", "high", "2026-01-15", "weekly", "work"
        )

        # Mark the task as complete
        completed_task = self.task_service.mark_task_complete(original_task.id)

        # Verify the original task is marked as complete
        assert completed_task.completed is True

        # Get all tasks to check if a new one was created
        all_tasks = self.task_service.get_all_tasks()
        incomplete_tasks = [task for task in all_tasks if not task.completed]

        # Should have 1 incomplete task (the new recurring instance)
        assert len(incomplete_tasks) == 1
        new_task = incomplete_tasks[0]

        # Verify the new task has the same properties as the original
        assert new_task.title == original_task.title
        assert new_task.description == original_task.description
        assert new_task.priority == original_task.priority
        assert new_task.category == original_task.category
        assert new_task.recurring_pattern == original_task.recurring_pattern

        # Verify the due date is updated for the next week
        assert new_task.due_date == "2026-01-22"

    def test_mark_task_complete_creates_new_recurring_task_monthly(self):
        """Test that marking a monthly recurring task as complete creates a new instance."""
        original_task = self.task_service.add_task(
            "Monthly review", "Review monthly goals", "high", "2026-01-15", "monthly", "work"
        )

        # Mark the task as complete
        completed_task = self.task_service.mark_task_complete(original_task.id)

        # Verify the original task is marked as complete
        assert completed_task.completed is True

        # Get all tasks to check if a new one was created
        all_tasks = self.task_service.get_all_tasks()
        incomplete_tasks = [task for task in all_tasks if not task.completed]

        # Should have 1 incomplete task (the new recurring instance)
        assert len(incomplete_tasks) == 1
        new_task = incomplete_tasks[0]

        # Verify the new task has the same properties as the original
        assert new_task.title == original_task.title
        assert new_task.description == original_task.description
        assert new_task.priority == original_task.priority
        assert new_task.category == original_task.category
        assert new_task.recurring_pattern == original_task.recurring_pattern

        # Verify the due date is updated for the next month
        assert new_task.due_date == "2026-02-15"

    def test_mark_task_complete_non_recurring_does_not_create_new_task(self):
        """Test that marking a non-recurring task as complete does not create a new instance."""
        original_task = self.task_service.add_task(
            "One time task", "Complete this once", "medium", "2026-01-15", "none", "other"
        )

        # Mark the task as complete
        completed_task = self.task_service.mark_task_complete(original_task.id)

        # Verify the original task is marked as complete
        assert completed_task.completed is True

        # Get all tasks to check if any new ones were created
        all_tasks = self.task_service.get_all_tasks()
        incomplete_tasks = [task for task in all_tasks if not task.completed]

        # Should have 0 incomplete tasks
        assert len(incomplete_tasks) == 0

    def test_mark_task_complete_no_due_date_recurring_does_not_create_new_task(self):
        """Test that marking a recurring task without due date as complete does not create a new instance."""
        original_task = self.task_service.add_task(
            "Daily habit", "Exercise daily", "medium", None, "daily", "home"
        )

        # Mark the task as complete
        completed_task = self.task_service.mark_task_complete(original_task.id)

        # Verify the original task is marked as complete
        assert completed_task.completed is True

        # Get all tasks to check if a new one was created
        all_tasks = self.task_service.get_all_tasks()
        incomplete_tasks = [task for task in all_tasks if not task.completed]

        # Should have 0 incomplete tasks since we can't calculate next due date without a current due date
        assert len(incomplete_tasks) == 0


class TestDueDateReminders:
    """Test class for due date reminder functionality."""

    def setup_method(self):
        """Set up a fresh TaskService instance for each test."""
        self.task_service = TaskService()

    def test_get_overdue_tasks_empty(self):
        """Test getting overdue tasks when there are none."""
        overdue_tasks = self.task_service.get_overdue_tasks()
        assert len(overdue_tasks) == 0

    def test_get_overdue_tasks_with_completed_tasks(self):
        """Test that completed tasks are not included in overdue tasks."""
        # Create a task that would be overdue but is completed
        past_date = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
        task = self.task_service.add_task("Completed past task", "Description", "high", past_date, "none", "work")
        self.task_service.mark_task_complete(task.id)

        overdue_tasks = self.task_service.get_overdue_tasks()
        assert len(overdue_tasks) == 0

    def test_get_overdue_tasks_includes_overdue_incomplete_tasks(self):
        """Test that overdue incomplete tasks are included."""
        # Create a task with a past due date that is not completed
        past_date = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
        task = self.task_service.add_task("Overdue task", "Description", "high", past_date, "none", "work")

        overdue_tasks = self.task_service.get_overdue_tasks()
        assert len(overdue_tasks) == 1
        assert overdue_tasks[0].id == task.id
        assert overdue_tasks[0].due_date == past_date
        assert overdue_tasks[0].completed is False

    def test_get_overdue_tasks_excludes_future_tasks(self):
        """Test that future tasks are not included in overdue tasks."""
        # Create a task with a future due date
        future_date = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
        task = self.task_service.add_task("Future task", "Description", "high", future_date, "none", "work")

        overdue_tasks = self.task_service.get_overdue_tasks()
        assert len(overdue_tasks) == 0

    def test_get_overdue_tasks_multiple(self):
        """Test getting multiple overdue tasks."""
        # Create multiple overdue tasks
        past_date1 = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
        past_date2 = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
        task1 = self.task_service.add_task("Overdue task 1", "Description", "high", past_date1, "none", "work")
        task2 = self.task_service.add_task("Overdue task 2", "Description", "medium", past_date2, "none", "home")

        overdue_tasks = self.task_service.get_overdue_tasks()
        assert len(overdue_tasks) == 2
        task_ids = [task.id for task in overdue_tasks]
        assert task1.id in task_ids
        assert task2.id in task_ids

    def test_get_upcoming_tasks_empty(self):
        """Test getting upcoming tasks when there are none."""
        upcoming_tasks = self.task_service.get_upcoming_tasks()
        assert len(upcoming_tasks) == 0

    def test_get_upcoming_tasks_default_days(self):
        """Test getting upcoming tasks with default 7 days."""
        # Create a task due in 3 days
        future_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
        task = self.task_service.add_task("Upcoming task", "Description", "high", future_date, "none", "work")

        upcoming_tasks = self.task_service.get_upcoming_tasks()
        assert len(upcoming_tasks) == 1
        assert upcoming_tasks[0].id == task.id

    def test_get_upcoming_tasks_custom_days(self):
        """Test getting upcoming tasks with custom number of days."""
        # Create a task due in 10 days
        future_date = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")
        task = self.task_service.add_task("Future task", "Description", "high", future_date, "none", "work")

        # Check with 15 days - should be included
        upcoming_tasks = self.task_service.get_upcoming_tasks(days=15)
        assert len(upcoming_tasks) == 1
        assert upcoming_tasks[0].id == task.id

        # Check with 5 days - should not be included
        upcoming_tasks = self.task_service.get_upcoming_tasks(days=5)
        assert len(upcoming_tasks) == 0

    def test_get_upcoming_tasks_excludes_overdue(self):
        """Test that overdue tasks are not included in upcoming tasks."""
        # Create a task with a past due date
        past_date = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
        task = self.task_service.add_task("Overdue task", "Description", "high", past_date, "none", "work")

        upcoming_tasks = self.task_service.get_upcoming_tasks()
        assert len(upcoming_tasks) == 0

    def test_get_upcoming_tasks_excludes_completed(self):
        """Test that completed tasks are not included in upcoming tasks."""
        # Create a task with a future due date but mark as completed
        future_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
        task = self.task_service.add_task("Completed task", "Description", "high", future_date, "none", "work")
        self.task_service.mark_task_complete(task.id)

        upcoming_tasks = self.task_service.get_upcoming_tasks()
        assert len(upcoming_tasks) == 0

    def test_get_due_tasks_for_date_empty(self):
        """Test getting tasks due on a specific date when there are none."""
        specific_date = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
        due_tasks = self.task_service.get_due_tasks_for_date(specific_date)
        assert len(due_tasks) == 0

    def test_get_due_tasks_for_date_matches(self):
        """Test getting tasks due on a specific date."""
        target_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
        task = self.task_service.add_task("Task for specific date", "Description", "high", target_date, "none", "work")

        due_tasks = self.task_service.get_due_tasks_for_date(target_date)
        assert len(due_tasks) == 1
        assert due_tasks[0].id == task.id
        assert due_tasks[0].due_date == target_date

    def test_get_due_tasks_for_date_excludes_other_dates(self):
        """Test that tasks due on other dates are not included."""
        target_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
        other_date = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")

        task1 = self.task_service.add_task("Task for target date", "Description", "high", target_date, "none", "work")
        task2 = self.task_service.add_task("Task for other date", "Description", "medium", other_date, "none", "home")

        due_tasks = self.task_service.get_due_tasks_for_date(target_date)
        assert len(due_tasks) == 1
        assert due_tasks[0].id == task1.id
        assert due_tasks[0].due_date == target_date

    def test_get_due_tasks_for_date_excludes_completed(self):
        """Test that completed tasks are not included in due tasks for date."""
        target_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
        task = self.task_service.add_task("Completed task", "Description", "high", target_date, "none", "work")
        self.task_service.mark_task_complete(task.id)

        due_tasks = self.task_service.get_due_tasks_for_date(target_date)
        assert len(due_tasks) == 0