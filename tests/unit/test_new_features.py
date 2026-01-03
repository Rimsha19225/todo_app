"""
Unit tests for the new features of the In-Memory Python Console Todo Application.
Tests for category, search, filter, and sort functionality.
"""

import pytest
from src.todo_app.services.task_service import TaskService
from src.todo_app.models.task import Task


class TestNewTaskFeatures:
    """Test class for new task features (category, search, filter, sort)."""

    def setup_method(self):
        """Set up a fresh TaskService instance for each test."""
        self.task_service = TaskService()

    def test_add_task_with_category(self):
        """Test adding a task with category."""
        task = self.task_service.add_task("Test Task", "Test Description", "high", "2026-12-31", "weekly", "work")

        assert task.category == "work"
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.priority == "high"
        assert task.due_date == "2026-12-31"
        assert task.recurring_pattern == "weekly"

    def test_category_validation(self):
        """Test that category values are validated correctly."""
        # Valid categories should work
        task1 = self.task_service.add_task("Task 1", category="work")
        task2 = self.task_service.add_task("Task 2", category="home")
        task3 = self.task_service.add_task("Task 3", category="other")

        assert task1.category == "work"
        assert task2.category == "home"
        assert task3.category == "other"

        # Invalid category should raise an error
        with pytest.raises(ValueError, match="Category must be one of"):
            self.task_service.add_task("Invalid Task", category="personal")

    def test_update_task_category(self):
        """Test updating task category."""
        task = self.task_service.add_task("Test Task", category="home")

        updated_task = self.task_service.update_task(task.id, category="work")

        assert updated_task is not None
        assert updated_task.category == "work"
        assert updated_task.title == "Test Task"

    def test_task_string_representation_with_category(self):
        """Test that the task string representation includes category."""
        task = self.task_service.add_task("Test Task", "Description", "high", "2026-12-31", "weekly", "work")

        task_str = str(task)
        assert "Test Task" in task_str
        assert "C:W" in task_str  # Work category should show as W

        task2 = self.task_service.add_task("Test Task 2", category="home")
        task_str2 = str(task2)
        assert "C:H" in task_str2  # Home category should show as H

    def test_default_category_value(self):
        """Test that tasks have correct default category value."""
        task = self.task_service.add_task("Test Task")

        assert task.category == "other"

    def test_get_all_tasks_includes_category(self):
        """Test that get_all_tasks returns tasks with category field."""
        task = self.task_service.add_task("Test Task", "Description", "high", "2026-12-31", "daily", "work")
        all_tasks = self.task_service.get_all_tasks()

        assert len(all_tasks) == 1
        retrieved_task = all_tasks[0]
        assert retrieved_task.category == "work"
        # Verify it's a different object (copy)
        assert retrieved_task is not task

    def test_get_task_by_id_includes_category(self):
        """Test that get_task_by_id returns tasks with category field."""
        task = self.task_service.add_task("Test Task", "Description", "low", "2026-06-15", "monthly", "home")
        retrieved_task = self.task_service.get_task_by_id(task.id)

        assert retrieved_task is not None
        assert retrieved_task.category == "home"
        # Verify it's a different object (copy)
        assert retrieved_task is not task


class TestSearchFunctionality:
    """Test class for search functionality."""

    def setup_method(self):
        """Set up a fresh TaskService instance for each test."""
        self.task_service = TaskService()

    def test_search_by_title(self):
        """Test searching tasks by title."""
        task1 = self.task_service.add_task("Work on project", "Important project work")
        task2 = self.task_service.add_task("Buy groceries", "Get food for the week")
        task3 = self.task_service.add_task("Fix bug", "Fix critical bug in app")

        results = self.task_service.search_tasks("project")
        assert len(results) == 1
        assert results[0].id == task1.id
        assert "project" in results[0].title.lower()

    def test_search_by_description(self):
        """Test searching tasks by description."""
        task1 = self.task_service.add_task("Task 1", "Important project work")
        task2 = self.task_service.add_task("Task 2", "Buy groceries for the week")
        task3 = self.task_service.add_task("Task 3", "Fix critical bug")

        results = self.task_service.search_tasks("groceries")
        assert len(results) == 1
        assert results[0].id == task2.id
        assert "groceries" in results[0].description.lower()

    def test_search_case_insensitive(self):
        """Test that search is case insensitive."""
        task1 = self.task_service.add_task("WORK on Project", "Important project work")
        task2 = self.task_service.add_task("Buy Groceries", "Get work done this week")  # Contains "work" in description

        results = self.task_service.search_tasks("work")
        assert len(results) == 2  # Both tasks should match
        result_ids = [task.id for task in results]
        assert task1.id in result_ids
        assert task2.id in result_ids

    def test_search_multiple_matches(self):
        """Test searching with multiple matches."""
        task1 = self.task_service.add_task("Work on project", "Important project work")
        task2 = self.task_service.add_task("Project meeting", "Discuss project updates")
        task3 = self.task_service.add_task("Fix bug", "Fix critical bug")

        results = self.task_service.search_tasks("project")
        assert len(results) == 2
        result_ids = [task.id for task in results]
        assert task1.id in result_ids
        assert task2.id in result_ids

    def test_search_no_matches(self):
        """Test searching with no matches."""
        self.task_service.add_task("Work on project", "Important project work")
        self.task_service.add_task("Buy groceries", "Get food for the week")

        results = self.task_service.search_tasks("nonexistent")
        assert len(results) == 0

    def test_search_empty_keyword(self):
        """Test searching with empty keyword."""
        self.task_service.add_task("Work on project", "Important project work")
        self.task_service.add_task("Buy groceries", "Get food for the week")

        results = self.task_service.search_tasks("")
        assert len(results) == 0

    def test_search_none_keyword(self):
        """Test searching with None keyword (should be treated as empty)."""
        self.task_service.add_task("Work on project", "Important project work")

        results = self.task_service.search_tasks(None)
        assert len(results) == 0


class TestFilterFunctionality:
    """Test class for filter functionality."""

    def setup_method(self):
        """Set up a fresh TaskService instance for each test."""
        self.task_service = TaskService()

    def test_filter_by_status_completed(self):
        """Test filtering tasks by completed status."""
        task1 = self.task_service.add_task("Completed task", "Description", "high")
        task2 = self.task_service.add_task("Incomplete task", "Description", "low")

        # Mark first task as completed
        self.task_service.mark_task_complete(task1.id)

        results = self.task_service.filter_tasks(status=True)
        assert len(results) == 1
        assert results[0].id == task1.id
        assert results[0].completed is True

    def test_filter_by_status_incomplete(self):
        """Test filtering tasks by incomplete status."""
        task1 = self.task_service.add_task("Completed task", "Description", "high")
        task2 = self.task_service.add_task("Incomplete task", "Description", "low")

        # Mark first task as completed
        self.task_service.mark_task_complete(task1.id)

        results = self.task_service.filter_tasks(status=False)
        assert len(results) == 1
        assert results[0].id == task2.id
        assert results[0].completed is False

    def test_filter_by_priority(self):
        """Test filtering tasks by priority."""
        task1 = self.task_service.add_task("High priority task", "Description", "high")
        task2 = self.task_service.add_task("Medium priority task", "Description", "medium")
        task3 = self.task_service.add_task("Low priority task", "Description", "low")

        results = self.task_service.filter_tasks(priority="high")
        assert len(results) == 1
        assert results[0].id == task1.id
        assert results[0].priority == "high"

        results = self.task_service.filter_tasks(priority="medium")
        assert len(results) == 1
        assert results[0].id == task2.id
        assert results[0].priority == "medium"

    def test_filter_by_due_date(self):
        """Test filtering tasks by due date."""
        task1 = self.task_service.add_task("Task 1", "Description", "high", "2026-01-01")
        task2 = self.task_service.add_task("Task 2", "Description", "low", "2026-12-31")
        task3 = self.task_service.add_task("Task 3", "Description", "medium")  # No due date

        results = self.task_service.filter_tasks(due_date="2026-01-01")
        assert len(results) == 1
        assert results[0].id == task1.id
        assert results[0].due_date == "2026-01-01"

    def test_filter_by_category(self):
        """Test filtering tasks by category."""
        task1 = self.task_service.add_task("Work task", "Description", "high", "2026-01-01", "none", "work")
        task2 = self.task_service.add_task("Home task", "Description", "low", "2026-12-31", "none", "home")
        task3 = self.task_service.add_task("Other task", "Description", "medium", None, "none", "other")

        results = self.task_service.filter_tasks(category="work")
        assert len(results) == 1
        assert results[0].id == task1.id
        assert results[0].category == "work"

        results = self.task_service.filter_tasks(category="home")
        assert len(results) == 1
        assert results[0].id == task2.id
        assert results[0].category == "home"

    def test_filter_by_multiple_criteria(self):
        """Test filtering tasks by multiple criteria."""
        task1 = self.task_service.add_task("Work task", "Description", "high", "2026-01-01", "none", "work")
        task2 = self.task_service.add_task("Home task", "Description", "low", "2026-12-31", "none", "home")
        task3 = self.task_service.add_task("Work urgent", "Description", "high", "2026-01-01", "none", "work")

        # Mark task3 as completed
        self.task_service.mark_task_complete(task3.id)

        # Filter by category=work and priority=high
        results = self.task_service.filter_tasks(category="work", priority="high")
        assert len(results) == 2
        result_ids = [task.id for task in results]
        assert task1.id in result_ids
        assert task3.id in result_ids

        # Filter by category=work, priority=high, and status=completed
        results = self.task_service.filter_tasks(category="work", priority="high", status=True)
        assert len(results) == 1
        assert results[0].id == task3.id
        assert results[0].completed is True

    def test_filter_no_matches(self):
        """Test filtering with criteria that match no tasks."""
        self.task_service.add_task("Task 1", "Description", "high", "2026-01-01", "none", "work")

        results = self.task_service.filter_tasks(priority="low")
        assert len(results) == 0

    def test_filter_with_none_criteria(self):
        """Test filtering with None criteria (should return all tasks)."""
        task1 = self.task_service.add_task("Task 1", "Description", "high", "2026-01-01", "none", "work")
        task2 = self.task_service.add_task("Task 2", "Description", "low", "2026-12-31", "none", "home")

        results = self.task_service.filter_tasks(status=None, priority=None, due_date=None, category=None)
        assert len(results) == 2


class TestSortFunctionality:
    """Test class for sort functionality."""

    def setup_method(self):
        """Set up a fresh TaskService instance for each test."""
        self.task_service = TaskService()

    def test_sort_by_title_ascending(self):
        """Test sorting tasks by title in ascending order."""
        task1 = self.task_service.add_task("Zebra task", "Description")
        task2 = self.task_service.add_task("Apple task", "Description")
        task3 = self.task_service.add_task("Mango task", "Description")

        results = self.task_service.sort_tasks(sort_by="title", ascending=True)
        assert len(results) == 3
        titles = [task.title for task in results]
        assert titles == ["Apple task", "Mango task", "Zebra task"]

    def test_sort_by_title_descending(self):
        """Test sorting tasks by title in descending order."""
        task1 = self.task_service.add_task("Apple task", "Description")
        task2 = self.task_service.add_task("Mango task", "Description")
        task3 = self.task_service.add_task("Zebra task", "Description")

        results = self.task_service.sort_tasks(sort_by="title", ascending=False)
        assert len(results) == 3
        titles = [task.title for task in results]
        assert titles == ["Zebra task", "Mango task", "Apple task"]

    def test_sort_by_priority(self):
        """Test sorting tasks by priority."""
        task1 = self.task_service.add_task("High priority", "Description", "high")
        task2 = self.task_service.add_task("Low priority", "Description", "low")
        task3 = self.task_service.add_task("Medium priority", "Description", "medium")

        results = self.task_service.sort_tasks(sort_by="priority", ascending=True)
        assert len(results) == 3
        priorities = [task.priority for task in results]
        assert priorities == ["high", "medium", "low"]  # high is first in our priority order

        results = self.task_service.sort_tasks(sort_by="priority", ascending=False)
        priorities = [task.priority for task in results]
        assert priorities == ["low", "medium", "high"]  # low is last in our priority order

    def test_sort_by_category(self):
        """Test sorting tasks by category."""
        task1 = self.task_service.add_task("Home task", "Description", "high", None, "none", "home")
        task2 = self.task_service.add_task("Work task", "Description", "low", None, "none", "work")
        task3 = self.task_service.add_task("Other task", "Description", "medium", None, "none", "other")

        results = self.task_service.sort_tasks(sort_by="category", ascending=True)
        assert len(results) == 3
        categories = [task.category for task in results]
        assert categories == ["work", "home", "other"]  # work is first in our category order

    def test_sort_by_status(self):
        """Test sorting tasks by status."""
        task1 = self.task_service.add_task("Incomplete task", "Description")
        task2 = self.task_service.add_task("Completed task", "Description")

        # Mark second task as completed
        self.task_service.mark_task_complete(task2.id)

        results = self.task_service.sort_tasks(sort_by="status", ascending=True)
        assert len(results) == 2
        statuses = [task.completed for task in results]
        assert statuses == [False, True]  # incomplete first, then completed

        results = self.task_service.sort_tasks(sort_by="status", ascending=False)
        statuses = [task.completed for task in results]
        assert statuses == [True, False]  # completed first, then incomplete

    def test_sort_by_due_date(self):
        """Test sorting tasks by due date."""
        task1 = self.task_service.add_task("Task 1", "Description", "high", "2026-12-31")
        task2 = self.task_service.add_task("Task 2", "Description", "low", "2026-01-01")
        task3 = self.task_service.add_task("Task 3", "Description", "medium")  # No due date

        results = self.task_service.sort_tasks(sort_by="due_date", ascending=True)
        assert len(results) == 3
        due_dates = [task.due_date for task in results]
        # None should come last, so we expect: 2026-01-01, 2026-12-31, None
        assert due_dates == ["2026-01-01", "2026-12-31", None]

    def test_sort_with_invalid_sort_by(self):
        """Test sorting with an invalid sort_by parameter."""
        task1 = self.task_service.add_task("Zebra task", "Description")
        task2 = self.task_service.add_task("Apple task", "Description")

        # Should default to sorting by title
        results = self.task_service.sort_tasks(sort_by="invalid", ascending=True)
        titles = [task.title for task in results]
        assert titles == ["Apple task", "Zebra task"]

    def test_sort_empty_list(self):
        """Test sorting an empty list of tasks."""
        results = self.task_service.sort_tasks(sort_by="title", ascending=True)
        assert len(results) == 0