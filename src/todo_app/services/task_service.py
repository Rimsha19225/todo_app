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

    def _validate_category(self, category: str) -> None:
        """Validate that the category is one of the allowed values."""
        valid_categories = ["work", "home", "other"]
        if category not in valid_categories:
            raise ValueError(f"Category must be one of {valid_categories}")

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

    def add_task(self, title: str, description: Optional[str] = "", priority: str = "medium", due_date: Optional[str] = None, recurring_pattern: str = "none", category: str = "other") -> Task:
        """
        Add a new task to the task list.

        Args:
            title (str): Required title of the task
            description (str, optional): Optional description of the task
            priority (str): Priority level of the task (high, medium, low), defaults to 'medium'
            due_date (str, optional): Due date of the task in YYYY-MM-DD format
            recurring_pattern (str): Recurring pattern of the task (daily, weekly, monthly, none), defaults to 'none'
            category (str): Category of the task (work, home, other), defaults to 'other'

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
        self._validate_category(category)
        self._validate_due_date(due_date)

        task_id = self._generate_id()
        new_task = Task(
            id=task_id,
            title=sanitized_title,
            description=sanitized_description,
            completed=False,
            priority=priority,
            due_date=due_date,
            recurring_pattern=recurring_pattern,
            category=category
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
                    due_date=task.due_date, recurring_pattern=task.recurring_pattern,
                    category=task.category)
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
                           due_date=task.due_date, recurring_pattern=task.recurring_pattern,
                           category=task.category)
        return None

    def update_task(self, task_id: str, title: Optional[str] = None, description: Optional[str] = None,
                   priority: Optional[str] = None, due_date: Optional[str] = None,
                   recurring_pattern: Optional[str] = None, category: Optional[str] = None) -> Optional[Task]:
        """
        Update an existing task with new information.

        Args:
            task_id (str): The ID of the task to update
            title (str, optional): New title for the task (if provided)
            description (str, optional): New description for the task (if provided)
            priority (str, optional): New priority level for the task (high, medium, low)
            due_date (str, optional): New due date for the task in YYYY-MM-DD format
            recurring_pattern (str, optional): New recurring pattern for the task (daily, weekly, monthly, none)
            category (str, optional): New category for the task (work, home, other)

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

        # Validate and update category if provided
        if category is not None:
            self._validate_category(category)
            original_task.category = category

        # Return a copy of the updated task
        return Task(id=original_task.id, title=original_task.title,
                   description=original_task.description, completed=original_task.completed,
                   priority=original_task.priority, due_date=original_task.due_date,
                   recurring_pattern=original_task.recurring_pattern, category=original_task.category)

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

    def _calculate_next_due_date(self, current_due_date: str, recurring_pattern: str) -> Optional[str]:
        """
        Calculate the next due date based on the recurring pattern.

        Args:
            current_due_date (str): The current due date in YYYY-MM-DD format
            recurring_pattern (str): The recurring pattern (daily, weekly, monthly)

        Returns:
            str or None: The next due date in YYYY-MM-DD format, or None if invalid
        """
        from datetime import datetime, timedelta

        if not current_due_date:
            return None

        try:
            current_date = datetime.strptime(current_due_date, "%Y-%m-%d")

            if recurring_pattern == "daily":
                next_date = current_date + timedelta(days=1)
            elif recurring_pattern == "weekly":
                next_date = current_date + timedelta(weeks=1)
            elif recurring_pattern == "monthly":
                # Calculate next month - handle month overflow
                if current_date.month == 12:
                    next_date = current_date.replace(year=current_date.year + 1, month=1)
                else:
                    next_date = current_date.replace(month=current_date.month + 1)
            else:
                return None  # No recurring pattern, return None

            return next_date.strftime("%Y-%m-%d")
        except ValueError:
            return None

    def mark_task_complete(self, task_id: str) -> Optional[Task]:
        """
        Mark a task as complete. If the task is recurring, create a new instance of the task
        with the next due date according to the recurring pattern.

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

        # Check if the task is recurring and needs to create a new instance
        if original_task.recurring_pattern != "none":
            # Calculate the next due date
            next_due_date = self._calculate_next_due_date(original_task.due_date, original_task.recurring_pattern)

            if next_due_date:
                # Create a new task with the same properties but updated due date
                new_task = Task(
                    id=self._generate_id(),
                    title=original_task.title,
                    description=original_task.description,
                    completed=False,  # New task starts as incomplete
                    priority=original_task.priority,
                    due_date=next_due_date,
                    recurring_pattern=original_task.recurring_pattern,
                    category=original_task.category
                )
                self._tasks.append(new_task)

        # Return a copy of the updated task
        return Task(id=original_task.id, title=original_task.title,
                   description=original_task.description, completed=original_task.completed,
                   priority=original_task.priority, due_date=original_task.due_date,
                   recurring_pattern=original_task.recurring_pattern, category=original_task.category)

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
                   description=original_task.description, completed=original_task.completed,
                   priority=original_task.priority, due_date=original_task.due_date,
                   recurring_pattern=original_task.recurring_pattern, category=original_task.category)

    def clear_all_tasks(self) -> None:
        """Clear all tasks from the task list."""
        self._tasks.clear()

    def search_tasks(self, keyword: str) -> List[Task]:
        """
        Search tasks by keyword in title or description.

        Args:
            keyword (str): The keyword to search for in task titles and descriptions

        Returns:
            List[Task]: A list of tasks that contain the keyword in their title or description
        """
        if not keyword:
            return []

        keyword_lower = keyword.lower()
        matching_tasks = []

        for task in self._tasks:
            # Check if keyword is in title or description (case-insensitive)
            if (keyword_lower in task.title.lower() or
                (task.description and keyword_lower in task.description.lower())):
                # Create a copy of the task to prevent external modifications
                matching_tasks.append(Task(
                    id=task.id,
                    title=task.title,
                    description=task.description,
                    completed=task.completed,
                    priority=task.priority,
                    due_date=task.due_date,
                    recurring_pattern=task.recurring_pattern,
                    category=task.category
                ))

        return matching_tasks

    def filter_tasks(self, status: Optional[bool] = None, priority: Optional[str] = None,
                    due_date: Optional[str] = None, category: Optional[str] = None) -> List[Task]:
        """
        Filter tasks by status, priority, due date, and/or category.

        Args:
            status (bool, optional): Filter by completion status (True for completed, False for incomplete)
            priority (str, optional): Filter by priority level (high, medium, low)
            due_date (str, optional): Filter by due date (YYYY-MM-DD format)
            category (str, optional): Filter by category (work, home, other)

        Returns:
            List[Task]: A list of tasks that match the specified filter criteria
        """
        filtered_tasks = []

        for task in self._tasks:
            # Check status filter
            if status is not None and task.completed != status:
                continue

            # Check priority filter
            if priority is not None and task.priority != priority:
                continue

            # Check due date filter
            if due_date is not None and task.due_date != due_date:
                continue

            # Check category filter
            if category is not None and task.category != category:
                continue

            # If all filters pass, add the task to the result
            # Create a copy of the task to prevent external modifications
            filtered_tasks.append(Task(
                id=task.id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                priority=task.priority,
                due_date=task.due_date,
                recurring_pattern=task.recurring_pattern,
                category=task.category
            ))

        return filtered_tasks

    def sort_tasks(self, sort_by: str = "title", ascending: bool = True) -> List[Task]:
        """
        Sort tasks by various criteria.

        Args:
            sort_by (str): Criteria to sort by ('title', 'priority', 'due_date', 'category', 'status')
            ascending (bool): Whether to sort in ascending order (default True)

        Returns:
            List[Task]: A list of tasks sorted by the specified criteria
        """
        # Create copies of tasks to prevent external modifications
        sorted_tasks = [Task(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            priority=task.priority,
            due_date=task.due_date,
            recurring_pattern=task.recurring_pattern,
            category=task.category
        ) for task in self._tasks]

        # Define priority and category order for proper sorting
        priority_order = {"high": 0, "medium": 1, "low": 2}
        category_order = {"work": 0, "home": 1, "other": 2}

        if sort_by == "title":
            sorted_tasks.sort(key=lambda x: x.title.lower(), reverse=not ascending)
        elif sort_by == "priority":
            sorted_tasks.sort(key=lambda x: priority_order.get(x.priority, 1), reverse=not ascending)
        elif sort_by == "due_date":
            # Sort by due date, with None values at the end
            sorted_tasks.sort(key=lambda x: (x.due_date is None, x.due_date), reverse=not ascending)
        elif sort_by == "category":
            sorted_tasks.sort(key=lambda x: category_order.get(x.category, 2), reverse=not ascending)
        elif sort_by == "status":
            # Sort by completion status (False = incomplete first, True = complete)
            sorted_tasks.sort(key=lambda x: x.completed, reverse=not ascending)
        else:
            # Default to sorting by title if invalid sort_by is provided
            sorted_tasks.sort(key=lambda x: x.title.lower(), reverse=not ascending)

        return sorted_tasks

    def get_overdue_tasks(self) -> List[Task]:
        """
        Get all tasks that are past their due date and not yet completed.

        Returns:
            List[Task]: A list of overdue tasks
        """
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")

        overdue_tasks = []
        for task in self._tasks:
            if (not task.completed and
                task.due_date and
                task.due_date < today):
                # Create a copy of the task to prevent external modifications
                overdue_tasks.append(Task(
                    id=task.id,
                    title=task.title,
                    description=task.description,
                    completed=task.completed,
                    priority=task.priority,
                    due_date=task.due_date,
                    recurring_pattern=task.recurring_pattern,
                    category=task.category
                ))

        return overdue_tasks

    def get_upcoming_tasks(self, days: int = 7) -> List[Task]:
        """
        Get all tasks that are due within the specified number of days.

        Args:
            days (int): Number of days to look ahead (default 7)

        Returns:
            List[Task]: A list of tasks due within the specified number of days
        """
        from datetime import datetime, timedelta
        today = datetime.now()
        future_date = today + timedelta(days=days)
        future_date_str = future_date.strftime("%Y-%m-%d")
        today_str = today.strftime("%Y-%m-%d")

        upcoming_tasks = []
        for task in self._tasks:
            if (not task.completed and
                task.due_date and
                today_str <= task.due_date <= future_date_str):
                # Create a copy of the task to prevent external modifications
                upcoming_tasks.append(Task(
                    id=task.id,
                    title=task.title,
                    description=task.description,
                    completed=task.completed,
                    priority=task.priority,
                    due_date=task.due_date,
                    recurring_pattern=task.recurring_pattern,
                    category=task.category
                ))

        return upcoming_tasks

    def get_due_tasks_for_date(self, date: str) -> List[Task]:
        """
        Get all tasks that are due on a specific date.

        Args:
            date (str): The date to check in YYYY-MM-DD format

        Returns:
            List[Task]: A list of tasks due on the specified date
        """
        due_tasks = []
        for task in self._tasks:
            if (not task.completed and
                task.due_date == date):
                # Create a copy of the task to prevent external modifications
                due_tasks.append(Task(
                    id=task.id,
                    title=task.title,
                    description=task.description,
                    completed=task.completed,
                    priority=task.priority,
                    due_date=task.due_date,
                    recurring_pattern=task.recurring_pattern,
                    category=task.category
                ))

        return due_tasks