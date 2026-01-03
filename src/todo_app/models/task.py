"""
Task model for the In-Memory Python Console Todo Application.

This module defines the Task class which represents a single todo item
with id, title, description, completion status, priority, due date, and recurring pattern attributes.

The Task class includes validation to ensure data integrity and provides
methods for string representation and dictionary conversion.
"""

from typing import Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Task:
    """
    Represents a single todo item in the application.

    Attributes:
        id (str): Unique identifier auto-generated when task is created
        title (str): Required title of the task
        description (str): Optional description of the task
        completed (bool): Status indicating if task is completed, defaults to False
        priority (str): Priority level of the task (high, medium, low), defaults to 'medium'
        due_date (str): Due date of the task in YYYY-MM-DD format, optional
        recurring_pattern (str): Recurring pattern of the task (daily, weekly, monthly, none), defaults to 'none'
        category (str): Category of the task (work, home, or other), defaults to 'other'
    """

    id: str
    title: str
    description: Optional[str] = ""
    completed: bool = False
    priority: str = "medium"
    due_date: Optional[str] = None
    recurring_pattern: str = "none"
    category: str = "other"

    def __post_init__(self):
        """Validate task attributes after initialization."""
        if not self.title or not self.title.strip():
            raise ValueError("Title must not be empty or null")
        if len(self.title) > 500:
            raise ValueError("Title must not exceed 500 characters")
        if len(self.description) > 2000:
            raise ValueError("Description must not exceed 2000 characters")
        if not isinstance(self.completed, bool):
            raise ValueError("Completed status must be a boolean value")

        # Validate priority
        valid_priorities = ["high", "medium", "low"]
        if self.priority not in valid_priorities:
            raise ValueError(f"Priority must be one of {valid_priorities}")

        # Validate recurring pattern
        valid_patterns = ["daily", "weekly", "monthly", "none"]
        if self.recurring_pattern not in valid_patterns:
            raise ValueError(f"Recurring pattern must be one of {valid_patterns}")

        # Validate category
        valid_categories = ["work", "home", "other"]
        if self.category not in valid_categories:
            raise ValueError(f"Category must be one of {valid_categories}")

        # Validate due date format if provided
        if self.due_date:
            try:
                datetime.strptime(self.due_date, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Due date must be in YYYY-MM-DD format")

    def __str__(self):
        """Return a string representation of the task."""
        status = "X" if self.completed else "O"
        priority_char = {"high": "H", "medium": "M", "low": "L"}.get(self.priority, "M")
        recurring_char = {"daily": "D", "weekly": "W", "monthly": "M", "none": "-"}.get(self.recurring_pattern, "-")
        category_char = {"work": "W", "home": "H", "other": "O"}.get(self.category, "O")

        result = f"[{status}] {self.id}: {self.title} (P:{priority_char}, C:{category_char})"
        if self.due_date:
            result += f" Due: {self.due_date}"
        if self.recurring_pattern != "none":
            result += f" Rec: {recurring_char}"
        if self.description:
            result += f" - {self.description}"
        return result

    def to_dict(self):
        """Convert the task to a dictionary representation."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "priority": self.priority,
            "due_date": self.due_date,
            "recurring_pattern": self.recurring_pattern,
            "category": self.category
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Task instance from a dictionary."""
        return cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            completed=data.get("completed", False),
            priority=data.get("priority", "medium"),
            due_date=data.get("due_date"),
            recurring_pattern=data.get("recurring_pattern", "none"),
            category=data.get("category", "other")
        )