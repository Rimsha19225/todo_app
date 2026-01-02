"""
Task service for the In-Memory Python Console Todo Application.

This module defines the TaskService class which handles all task operations
including add, update, delete, mark complete/incomplete, and retrieval.
"""

from typing import List, Optional
from src.todo_app.models.task import Task


class TaskService:
    """
    Service class that handles all task operations for the todo application.
    Uses in-memory storage to store tasks during application runtime.
    """

    def __init__(self):
        """Initialize the task service with an empty in-memory storage."""
        self._tasks: List[Task] = []
        self._next_id = 1

    def _generate_id(self) -> str:
        """Generate a unique ID for a new task."""
        new_id = str(self._next_id)
        self._next_id += 1
        return new_id

    def _validate_title(self, title: str) -> None:
        """Validate that the title is not empty and not too long."""
        if not title or not title.strip():
            raise ValueError("Title must not be empty or null")
        if len(title) > 500:
            raise ValueError("Title must not exceed 500 characters")

    def _validate_description(self, description: str) -> None:
        """Validate that the description is not too long."""
        if len(description) > 2000:
            raise ValueError("Description must not exceed 2000 characters")

    def _validate_priority(self, priority: str) -> None:
        """Validate that the priority is one of the allowed values."""
        valid_priorities = ["high", "medium", "low"]
        if priority not in valid_priorities:
            raise ValueError(f"Priority must be one of {valid_priorities}")

    def _validate_recurring_pattern(self, pattern: str) -> None:
        """Validate that the recurring pattern is one of the allowed values."""
        valid_patterns = ["daily", "weekly", "monthly", "none"]
        if pattern not in valid_patterns:
            raise ValueError(f"Recurring pattern must be one of {valid_patterns}")

    def _validate_due_date(self, due_date: str) -> None:
        """Validate that the due date is in the correct format."""
        if due_date:
            from datetime import datetime
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Due date must be in YYYY-MM-DD format")

    def _sanitize_input(self, text: str) -> str:
        """
        Sanitize input text by removing potentially harmful characters.

        Args:
            text (str): The input text to sanitize

        Returns:
            str: The sanitized text
        """
        # Handle None case - should be caught by validation later
        if text is None:
            return ""
        # For now, just strip leading/trailing whitespace
        # In a more complex system, we might want to remove/escape special characters
        return text.strip()

    def add_task(self, title: str, description: Optional[str] = "", priority: str = "medium", due_date: Optional[str] = None, recurring_pattern: str = "none") -> Task:
        """
        Add a new task to the task list.

        Args:
            title (str): Required title of the task
            description (str, optional): Optional description of the task
            priority (str): Priority level of the task (high, medium, low), defaults to 'medium'
            due_date (str, optional): Due date of the task in YYYY-MM-DD format
            recurring_pattern (str): Recurring pattern of the task (daily, weekly, monthly, none), defaults to 'none'

        Returns:
            Task: The newly created task with auto-generated ID and default completion status

        Raises:
            ValueError: If title is empty, null, exceeds length limits, or other validation fails
        """
        # Sanitize inputs
        sanitized_title = self._sanitize_input(title)
        sanitized_description = self._sanitize_input(description or "")

        self._validate_title(sanitized_title)
        self._validate_description(sanitized_description)
        self._validate_priority(priority)
        self._validate_recurring_pattern(recurring_pattern)
        self._validate_due_date(due_date)

        task_id = self._generate_id()
        new_task = Task(
            id=task_id,
            title=sanitized_title,
            description=sanitized_description,
            completed=False,
            priority=priority,
            due_date=due_date,
            recurring_pattern=recurring_pattern
        )
        self._tasks.append(new_task)
        return new_task

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks from the task list.

        Returns:
            List[Task]: A list of all tasks in the application
        """
        # Return copies of tasks to prevent external modifications
        return [Task(id=task.id, title=task.title, description=task.description,
                    completed=task.completed, priority=task.priority,
                    due_date=task.due_date, recurring_pattern=task.recurring_pattern)
                for task in self._tasks]

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """
        Retrieve a task by its ID.

        Args:
            task_id (str): The ID of the task to retrieve

        Returns:
            Task or None: The task with the specified ID, or None if not found
        """
        for task in self._tasks:
            if task.id == task_id:
                # Return a copy of the task to prevent external modifications
                return Task(id=task.id, title=task.title, description=task.description,
                           completed=task.completed, priority=task.priority,
                           due_date=task.due_date, recurring_pattern=task.recurring_pattern)
        return None

    def update_task(self, task_id: str, title: Optional[str] = None, description: Optional[str] = None,
                   priority: Optional[str] = None, due_date: Optional[str] = None,
                   recurring_pattern: Optional[str] = None) -> Optional[Task]:
        """
        Update an existing task with new information.

        Args:
            task_id (str): The ID of the task to update
            title (str, optional): New title for the task (if provided)
            description (str, optional): New description for the task (if provided)
            priority (str, optional): New priority level for the task (high, medium, low)
            due_date (str, optional): New due date for the task in YYYY-MM-DD format
            recurring_pattern (str, optional): New recurring pattern for the task (daily, weekly, monthly, none)

        Returns:
            Task or None: The updated task if found, or None if task ID doesn't exist
        """
        # Find the original task in the internal list
        original_task_index = None
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                original_task_index = i
                break

        if original_task_index is None:
            return None

        # Get the original task
        original_task = self._tasks[original_task_index]

        # Validate and update title if provided
        if title is not None:
            sanitized_title = self._sanitize_input(title)
            self._validate_title(sanitized_title)
            original_task.title = sanitized_title

        # Validate and update description if provided
        if description is not None:
            sanitized_description = self._sanitize_input(description)
            self._validate_description(sanitized_description)
            original_task.description = sanitized_description

        # Validate and update priority if provided
        if priority is not None:
            self._validate_priority(priority)
            original_task.priority = priority

        # Validate and update due_date if provided
        if due_date is not None:
            self._validate_due_date(due_date)
            original_task.due_date = due_date

        # Validate and update recurring_pattern if provided
        if recurring_pattern is not None:
            self._validate_recurring_pattern(recurring_pattern)
            original_task.recurring_pattern = recurring_pattern

        # Return a copy of the updated task
        return Task(id=original_task.id, title=original_task.title,
                   description=original_task.description, completed=original_task.completed,
                   priority=original_task.priority, due_date=original_task.due_date,
                   recurring_pattern=original_task.recurring_pattern)

    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id (str): The ID of the task to delete

        Returns:
            bool: True if the task was found and deleted, False if not found
        """
        task = self.get_task_by_id(task_id)
        if task:
            self._tasks.remove(task)
            return True
        return False

    def mark_task_complete(self, task_id: str) -> Optional[Task]:
        """
        Mark a task as complete.

        Args:
            task_id (str): The ID of the task to mark as complete

        Returns:
            Task or None: The updated task if found, or None if task ID doesn't exist
        """
        # Find the original task in the internal list
        original_task_index = None
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                original_task_index = i
                break

        if original_task_index is None:
            return None

        # Get the original task and update it
        original_task = self._tasks[original_task_index]
        original_task.completed = True

        # Return a copy of the updated task
        return Task(id=original_task.id, title=original_task.title,
                   description=original_task.description, completed=original_task.completed)

    def mark_task_incomplete(self, task_id: str) -> Optional[Task]:
        """
        Mark a task as incomplete.

        Args:
            task_id (str): The ID of the task to mark as incomplete

        Returns:
            Task or None: The updated task if found, or None if task ID doesn't exist
        """
        # Find the original task in the internal list
        original_task_index = None
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                original_task_index = i
                break

        if original_task_index is None:
            return None

        # Get the original task and update it
        original_task = self._tasks[original_task_index]
        original_task.completed = False

        # Return a copy of the updated task
        return Task(id=original_task.id, title=original_task.title,
                   description=original_task.description, completed=original_task.completed)

    def clear_all_tasks(self) -> None:
        """Clear all tasks from the task list."""
        self._tasks.clear()