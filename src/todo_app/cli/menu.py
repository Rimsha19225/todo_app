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
        print("6. Exit")
        print("="*50)

    def get_user_choice(self) -> str:
        """
        Get the user's menu choice.

        Returns:
            str: The user's menu choice
        """
        try:
            choice = input("Enter your choice (1-6): ").strip()
            return choice
        except (EOFError, KeyboardInterrupt):
            print("\nExiting application...")
            return "6"  # Return exit choice

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

            task = self.task_service.add_task(title, description, priority, due_date, recurring_pattern)
            print(f"Task added successfully with ID: {task.id}")
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

            updated_task = self.task_service.update_task(
                task_id,
                updated_title,
                updated_description,
                updated_priority,
                updated_due_date,
                updated_recurring_pattern
            )
            if updated_task:
                print(f"Task updated successfully!")
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
                print("\nThank you for using the Todo Application. Goodbye!")
                break
            else:
                print(f"\nInvalid choice: {choice}. Please enter a number between 1-6.")