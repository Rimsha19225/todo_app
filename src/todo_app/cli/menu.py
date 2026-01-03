"""
CLI menu interface for the In-Memory Python Console Todo Application.

This module defines the Menu class which handles the console-based user interface
with numbered menu options for all user stories.
"""

from typing import Optional
from src.todo_app.services.task_service import TaskService


class Menu:
    """
    Console-based menu interface for the todo application.
    Provides numbered menu options for all user stories.
    """

    def __init__(self, task_service: TaskService):
        """
        Initialize the menu with a task service.

        Args:
            task_service (TaskService): The service to handle task operations
        """
        self.task_service = task_service

    def display_menu(self):
        """Display the main menu options to the user."""
        print("\n" + "="*50)
        print("Welcome to the Todo Application!")
        print("="*50)
        print("Please select an option:")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Task Complete/Incomplete")
        print("6. Search Tasks")
        print("7. Filter Tasks")
        print("8. Sort Tasks")
        print("9. View Overdue Tasks")
        print("10. View Upcoming Tasks")
        print("11. Exit")
        print("="*50)

    def get_user_choice(self) -> str:
        """
        Get the user's menu choice.

        Returns:
            str: The user's menu choice
        """
        try:
            choice = input("Enter your choice (1-11): ").strip()
            return choice
        except (EOFError, KeyboardInterrupt):
            print("\nExiting application...")
            return "11"  # Return exit choice

    def handle_add_task(self):
        """Handle the add task menu option."""
        print("\n--- Add Task ---")
        try:
            title = input("Enter task title (required): ").strip()
            if not title:
                print("Error: Title is required and cannot be empty.")
                return

            description = input("Enter task description (optional, press Enter to skip): ").strip()
            if not description:  # If user just pressed Enter, use empty string
                description = ""

            # Get priority
            print("Select priority level:")
            print("1. High")
            print("2. Medium (default)")
            print("3. Low")
            priority_choice = input("Enter choice (1-3, default 2): ").strip()
            priority_map = {"1": "high", "2": "medium", "3": "low"}
            priority = priority_map.get(priority_choice, "medium")

            # Get due date
            due_date = input("Enter due date (YYYY-MM-DD format, optional, press Enter to skip): ").strip()
            if not due_date:
                due_date = None

            # Get recurring pattern
            print("Select recurring pattern:")
            print("1. Daily")
            print("2. Weekly")
            print("3. Monthly")
            print("4. None (default)")
            recurring_choice = input("Enter choice (1-4, default 4): ").strip()
            recurring_map = {"1": "daily", "2": "weekly", "3": "monthly", "4": "none"}
            recurring_pattern = recurring_map.get(recurring_choice, "none")

            # Get category
            print("Select category:")
            print("1. Work")
            print("2. Home")
            print("3. Other (default)")
            category_choice = input("Enter choice (1-3, default 3): ").strip()
            category_map = {"1": "work", "2": "home", "3": "other"}
            category = category_map.get(category_choice, "other")

            task = self.task_service.add_task(title, description, priority, due_date, recurring_pattern, category)
            print(f"Task added successfully with ID: {task.id}")
            print(f"Task details: {task}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def handle_view_all_tasks(self):
        """Handle the view all tasks menu option."""
        print("\n--- All Tasks ---")
        tasks = self.task_service.get_all_tasks()

        if not tasks:
            print("No tasks found.")
            return

        for task in tasks:
            status = "✓" if task.completed else "○"
            print(f"[{status}] ID: {task.id} | Title: {task.title}")
            if task.description:
                print(f"    Description: {task.description}")
            print(f"    Priority: {task.priority} | Category: {task.category}")
            if task.due_date:
                print(f"    Due: {task.due_date}")
            print("-" * 40)

    def handle_update_task(self):
        """Handle the update task menu option."""
        print("\n--- Update Task ---")
        try:
            task_id = input("Enter task ID to update: ").strip()
            if not task_id:
                print("Error: Task ID is required.")
                return

            existing_task = self.task_service.get_task_by_id(task_id)
            if not existing_task:
                print(f"Error: Task with ID {task_id} not found.")
                return

            print(f"Current task: {existing_task.title}")

            # Update title
            new_title = input(f"Enter new title (current: '{existing_task.title}', press Enter to keep current): ").strip()
            updated_title = new_title if new_title else existing_task.title

            # Update description
            new_description = input(f"Enter new description (current: '{existing_task.description}', press Enter to keep current): ").strip()
            updated_description = new_description if new_description else existing_task.description

            # Update priority
            print(f"Current priority: {existing_task.priority}")
            print("Select new priority level (or press Enter to keep current):")
            print("1. High")
            print("2. Medium")
            print("3. Low")
            priority_choice = input("Enter choice (1-3, or press Enter to keep current): ").strip()
            priority_map = {"1": "high", "2": "medium", "3": "low"}
            updated_priority = priority_map.get(priority_choice, existing_task.priority if not priority_choice else existing_task.priority)

            # Update due date
            print(f"Current due date: {existing_task.due_date if existing_task.due_date else 'None'}")
            new_due_date_input = input("Enter new due date (YYYY-MM-DD format, or press Enter to keep current): ").strip()
            updated_due_date = existing_task.due_date  # Default to existing value
            if new_due_date_input:  # If user provided a new value
                updated_due_date = new_due_date_input

            # Update recurring pattern
            print(f"Current recurring pattern: {existing_task.recurring_pattern}")
            print("Select new recurring pattern (or press Enter to keep current):")
            print("1. Daily")
            print("2. Weekly")
            print("3. Monthly")
            print("4. None")
            recurring_choice = input("Enter choice (1-4, or press Enter to keep current): ").strip()
            recurring_map = {"1": "daily", "2": "weekly", "3": "monthly", "4": "none"}
            updated_recurring_pattern = recurring_map.get(recurring_choice, existing_task.recurring_pattern if not recurring_choice else existing_task.recurring_pattern)

            # Update category
            print(f"Current category: {existing_task.category}")
            print("Select new category (or press Enter to keep current):")
            print("1. Work")
            print("2. Home")
            print("3. Other")
            category_choice = input("Enter choice (1-3, or press Enter to keep current): ").strip()
            category_map = {"1": "work", "2": "home", "3": "other"}
            updated_category = category_map.get(category_choice, existing_task.category if not category_choice else existing_task.category)

            updated_task = self.task_service.update_task(
                task_id,
                updated_title,
                updated_description,
                updated_priority,
                updated_due_date,
                updated_recurring_pattern,
                updated_category
            )
            if updated_task:
                print(f"Task updated successfully!")
                print(f"Updated task details: {updated_task}")
            else:
                print(f"Error: Failed to update task with ID {task_id}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def handle_delete_task(self):
        """Handle the delete task menu option."""
        print("\n--- Delete Task ---")
        try:
            task_id = input("Enter task ID to delete: ").strip()
            if not task_id:
                print("Error: Task ID is required.")
                return

            success = self.task_service.delete_task(task_id)
            if success:
                print(f"Task with ID {task_id} deleted successfully!")
            else:
                print(f"Error: Task with ID {task_id} not found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def handle_mark_task(self):
        """Handle the mark task complete/incomplete menu option."""
        print("\n--- Mark Task Complete/Incomplete ---")
        try:
            task_id = input("Enter task ID: ").strip()
            if not task_id:
                print("Error: Task ID is required.")
                return

            existing_task = self.task_service.get_task_by_id(task_id)
            if not existing_task:
                print(f"Error: Task with ID {task_id} not found.")
                return

            print(f"Current status: {'Completed' if existing_task.completed else 'Incomplete'}")
            choice = input("Mark as (1) Complete or (2) Incomplete: ").strip()

            if choice == "1":
                updated_task = self.task_service.mark_task_complete(task_id)
                if updated_task:
                    print(f"Task marked as complete!")
                else:
                    print(f"Error: Failed to mark task as complete.")
            elif choice == "2":
                updated_task = self.task_service.mark_task_incomplete(task_id)
                if updated_task:
                    print(f"Task marked as incomplete!")
                else:
                    print(f"Error: Failed to mark task as incomplete.")
            else:
                print("Error: Invalid choice. Please enter 1 or 2.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def handle_search_tasks(self):
        """Handle the search tasks menu option."""
        print("\n--- Search Tasks ---")
        try:
            keyword = input("Enter keyword to search for in title or description: ").strip()
            if not keyword:
                print("Error: Keyword is required.")
                return

            tasks = self.task_service.search_tasks(keyword)

            if not tasks:
                print("No tasks found matching the keyword.")
                return

            print(f"Found {len(tasks)} task(s) matching '{keyword}':")
            for task in tasks:
                status = "✓" if task.completed else "○"
                print(f"[{status}] ID: {task.id} | Title: {task.title}")
                if task.description:
                    print(f"    Description: {task.description}")
                print(f"    Priority: {task.priority} | Category: {task.category}")
                if task.due_date:
                    print(f"    Due: {task.due_date}")
                print("-" * 40)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def handle_filter_tasks(self):
        """Handle the filter tasks menu option."""
        print("\n--- Filter Tasks ---")
        try:
            print("Enter filter criteria (press Enter to skip each):")

            # Get status filter
            status_input = input("Filter by status (c for completed, i for incomplete, Enter to skip): ").strip().lower()
            status = None
            if status_input == "c":
                status = True
            elif status_input == "i":
                status = False

            # Get priority filter
            priority_input = input("Filter by priority (high/medium/low, Enter to skip): ").strip().lower()
            priority = priority_input if priority_input in ["high", "medium", "low"] else None

            # Get due date filter
            due_date = input("Filter by due date (YYYY-MM-DD format, Enter to skip): ").strip()
            due_date = due_date if due_date else None

            # Get category filter
            category_input = input("Filter by category (work/home/other, Enter to skip): ").strip().lower()
            category = category_input if category_input in ["work", "home", "other"] else None

            tasks = self.task_service.filter_tasks(status=status, priority=priority,
                                                 due_date=due_date, category=category)

            if not tasks:
                print("No tasks found matching the filter criteria.")
                return

            print(f"Found {len(tasks)} task(s) matching the filter criteria:")
            for task in tasks:
                status = "✓" if task.completed else "○"
                print(f"[{status}] ID: {task.id} | Title: {task.title}")
                if task.description:
                    print(f"    Description: {task.description}")
                print(f"    Priority: {task.priority} | Category: {task.category}")
                if task.due_date:
                    print(f"    Due: {task.due_date}")
                print("-" * 40)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def handle_sort_tasks(self):
        """Handle the sort tasks menu option."""
        print("\n--- Sort Tasks ---")
        try:
            print("Sort by:")
            print("1. Title (alphabetically)")
            print("2. Priority")
            print("3. Due Date")
            print("4. Category")
            print("5. Status")

            sort_choice = input("Enter choice (1-5): ").strip()

            sort_options = {
                "1": "title",
                "2": "priority",
                "3": "due_date",
                "4": "category",
                "5": "status"
            }

            sort_by = sort_options.get(sort_choice, "title")

            order_choice = input("Sort order (a for ascending, d for descending): ").strip().lower()
            ascending = True if order_choice == "a" else False

            tasks = self.task_service.sort_tasks(sort_by=sort_by, ascending=ascending)

            if not tasks:
                print("No tasks to display.")
                return

            print(f"Tasks sorted by {sort_by} ({'ascending' if ascending else 'descending'}):")
            for task in tasks:
                status = "✓" if task.completed else "○"
                print(f"[{status}] ID: {task.id} | Title: {task.title}")
                if task.description:
                    print(f"    Description: {task.description}")
                print(f"    Priority: {task.priority} | Category: {task.category}")
                if task.due_date:
                    print(f"    Due: {task.due_date}")
                print("-" * 40)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def handle_view_overdue_tasks(self):
        """Handle the view overdue tasks menu option."""
        print("\n--- Overdue Tasks ---")
        try:
            tasks = self.task_service.get_overdue_tasks()

            if not tasks:
                print("No overdue tasks found.")
                return

            print(f"Found {len(tasks)} overdue task(s):")
            for task in tasks:
                print(f"ID: {task.id} | Title: {task.title}")
                if task.description:
                    print(f"    Description: {task.description}")
                print(f"    Priority: {task.priority} | Category: {task.category}")
                if task.due_date:
                    print(f"    Due: {task.due_date}")
                print("-" * 40)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def handle_view_upcoming_tasks(self):
        """Handle the view upcoming tasks menu option."""
        print("\n--- Upcoming Tasks ---")
        try:
            days_input = input("Enter number of days to look ahead (default 7): ").strip()
            try:
                days = int(days_input) if days_input else 7
            except ValueError:
                days = 7
                print(f"Invalid input. Using default value of {days} days.")

            tasks = self.task_service.get_upcoming_tasks(days=days)

            if not tasks:
                print(f"No tasks due in the next {days} day(s).")
                return

            print(f"Found {len(tasks)} task(s) due in the next {days} day(s):")
            for task in tasks:
                print(f"ID: {task.id} | Title: {task.title}")
                if task.description:
                    print(f"    Description: {task.description}")
                print(f"    Priority: {task.priority} | Category: {task.category}")
                if task.due_date:
                    print(f"    Due: {task.due_date}")
                print("-" * 40)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def run(self):
        """Run the main menu loop."""
        print("Starting Todo Application...")
        while True:
            self.display_menu()
            choice = self.get_user_choice()

            if choice == "1":
                self.handle_add_task()
            elif choice == "2":
                self.handle_view_all_tasks()
            elif choice == "3":
                self.handle_update_task()
            elif choice == "4":
                self.handle_delete_task()
            elif choice == "5":
                self.handle_mark_task()
            elif choice == "6":
                self.handle_search_tasks()
            elif choice == "7":
                self.handle_filter_tasks()
            elif choice == "8":
                self.handle_sort_tasks()
            elif choice == "9":
                self.handle_view_overdue_tasks()
            elif choice == "10":
                self.handle_view_upcoming_tasks()
            elif choice == "11":
                print("\nThank you for using the Todo Application. Goodbye!")
                break
            else:
                print(f"\nInvalid choice: {choice}. Please enter a number between 1-11.")