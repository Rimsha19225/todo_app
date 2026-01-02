"""
Main entry point for the In-Memory Python Console Todo Application.

This module initializes the application components and starts the main menu loop.
"""

from src.todo_app.services.task_service import TaskService
from src.todo_app.cli.menu import Menu


def main():
    """
    Main function to run the todo application.
    Initializes the task service and menu, then starts the application loop.
    """
    # Initialize the task service
    task_service = TaskService()

    # Initialize the menu with the task service
    menu = Menu(task_service)

    # Start the application
    menu.run()


if __name__ == "__main__":
    main()