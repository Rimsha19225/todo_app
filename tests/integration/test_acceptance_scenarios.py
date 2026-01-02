"""
Tests for acceptance scenarios from the specification in the In-Memory Python Console Todo Application.
"""

import pytest
from src.todo_app.services.task_service import TaskService


class TestAcceptanceScenarios:
    """Tests for acceptance scenarios from the specification."""

    def setup_method(self):
        """Set up a fresh TaskService instance for each test."""
        self.task_service = TaskService()

    def test_acceptance_scenario_user_story_1_1(self):
        """
        Acceptance Scenario 1 for User Story 1:
        Given I am at the main menu, When I choose to add a task and provide a title,
        Then the task is added to my list with a unique ID and marked as incomplete
        """
        task = self.task_service.add_task("Buy groceries")

        assert task.title == "Buy groceries"
        assert task.id == "1"  # First task gets ID "1"
        assert task.completed is False

    def test_acceptance_scenario_user_story_1_2(self):
        """
        Acceptance Scenario 2 for User Story 1:
        Given I am adding a task, When I provide only a title (no description),
        Then the task is added with the title and an empty description field
        """
        task = self.task_service.add_task("Buy groceries")

        assert task.title == "Buy groceries"
        assert task.description == ""
        assert task.completed is False

    def test_acceptance_scenario_user_story_1_3(self):
        """
        Acceptance Scenario 3 for User Story 1:
        Given I am adding a task, When I provide both a title and description,
        Then the task is added with both fields populated
        """
        task = self.task_service.add_task("Buy groceries", "Milk, bread, eggs")

        assert task.title == "Buy groceries"
        assert task.description == "Milk, bread, eggs"
        assert task.completed is False

    def test_acceptance_scenario_user_story_2_1(self):
        """
        Acceptance Scenario 1 for User Story 2:
        Given I have added tasks to my list, When I choose to view all tasks,
        Then I see a formatted list showing all tasks with their ID, title, description, and completion status
        """
        task1 = self.task_service.add_task("Task 1", "Description 1")
        task2 = self.task_service.add_task("Task 2", "Description 2")

        all_tasks = self.task_service.get_all_tasks()

        assert len(all_tasks) == 2
        assert all_tasks[0].title == "Task 1"
        assert all_tasks[0].description == "Description 1"
        assert all_tasks[0].completed is False
        assert all_tasks[0].id == task1.id

        assert all_tasks[1].title == "Task 2"
        assert all_tasks[1].description == "Description 2"
        assert all_tasks[1].completed is False
        assert all_tasks[1].id == task2.id

    def test_acceptance_scenario_user_story_2_2(self):
        """
        Acceptance Scenario 2 for User Story 2:
        Given I have no tasks in my list, When I choose to view all tasks,
        Then I see a message indicating there are no tasks
        """
        all_tasks = self.task_service.get_all_tasks()

        assert len(all_tasks) == 0

    def test_acceptance_scenario_user_story_3_1(self):
        """
        Acceptance Scenario 1 for User Story 3:
        Given I have tasks in my list, When I choose to update a task by its ID and provide new details,
        Then the task is updated with the new information
        """
        task = self.task_service.add_task("Old Title", "Old Description")

        updated_task = self.task_service.update_task(task.id, "New Title", "New Description")

        assert updated_task is not None
        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"

    def test_acceptance_scenario_user_story_3_2(self):
        """
        Acceptance Scenario 2 for User Story 3:
        Given I attempt to update a task with an invalid ID, When I enter the ID,
        Then I receive a clear error message indicating the task does not exist
        """
        result = self.task_service.update_task("999", "New Title")

        assert result is None

    def test_acceptance_scenario_user_story_4_1(self):
        """
        Acceptance Scenario 1 for User Story 4:
        Given I have tasks in my list, When I choose to delete a task by its ID,
        Then the task is removed from the list
        """
        task = self.task_service.add_task("Task to delete")

        success = self.task_service.delete_task(task.id)

        assert success is True
        all_tasks = self.task_service.get_all_tasks()
        assert len(all_tasks) == 0

    def test_acceptance_scenario_user_story_4_2(self):
        """
        Acceptance Scenario 2 for User Story 4:
        Given I attempt to delete a task with an invalid ID, When I enter the ID,
        Then I receive a clear error message indicating the task does not exist
        """
        success = self.task_service.delete_task("999")

        assert success is False

    def test_acceptance_scenario_user_story_5_1(self):
        """
        Acceptance Scenario 1 for User Story 5:
        Given I have tasks in my list, When I choose to mark a task as complete by its ID,
        Then the task's status is updated to completed
        """
        task = self.task_service.add_task("Task to complete")

        updated_task = self.task_service.mark_task_complete(task.id)

        assert updated_task is not None
        assert updated_task.completed is True

    def test_acceptance_scenario_user_story_5_2(self):
        """
        Acceptance Scenario 2 for User Story 5:
        Given I have completed tasks in my list, When I choose to mark a task as incomplete by its ID,
        Then the task's status is updated to not completed
        """
        task = self.task_service.add_task("Task to complete")
        self.task_service.mark_task_complete(task.id)  # Mark it complete first

        updated_task = self.task_service.mark_task_incomplete(task.id)

        assert updated_task is not None
        assert updated_task.completed is False

    def test_acceptance_scenario_user_story_5_3(self):
        """
        Acceptance Scenario 3 for User Story 5:
        Given I attempt to mark a task with an invalid ID, When I enter the ID,
        Then I receive a clear error message indicating the task does not exist
        """
        result = self.task_service.mark_task_complete("999")

        assert result is None