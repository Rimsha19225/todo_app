# Quickstart Guide: In-Memory Python Console Todo Application

**Feature**: 1-todo-app
**Date**: 2026-01-03
**Status**: Complete

## Overview

This quickstart guide provides instructions for setting up and running the In-Memory Python Console Todo Application. The application is a simple console-based todo manager that stores tasks in memory only.

## Prerequisites

- Python 3.8 or higher
- No additional dependencies required (uses only Python standard library)

## Installation

1. Clone or download the project repository
2. Navigate to the project directory
3. Ensure Python 3.8+ is installed on your system

## Running the Application

1. Navigate to the project root directory
2. Run the application using Python:
   ```bash
   python -m src.todo_app.main
   ```

   Or if the application is structured as a module:
   ```bash
   python -m todo_app
   ```

## Using the Application

Once the application starts, you will see a numbered menu with the following options:

1. **Add Task** - Create a new todo task
   - Enter a title (required)
   - Optionally enter a description
   - The system will assign a unique ID

2. **View All Tasks** - Display all tasks in your list
   - Shows ID, title, description, and completion status
   - Tasks are displayed in a formatted list

3. **Update Task** - Modify an existing task
   - Enter the task ID
   - Provide new title and/or description
   - The system will update the specified task

4. **Delete Task** - Remove a task from your list
   - Enter the task ID
   - The system will remove the specified task

5. **Mark Task Complete/Incomplete** - Update task status
   - Enter the task ID
   - Choose to mark as complete or incomplete
   - The system will update the completion status

6. **Exit** - Quit the application
   - The application will terminate
   - Note: All data will be lost as it's stored in memory only

## Example Usage

```
Welcome to the Todo Application!
Please select an option:
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete/Incomplete
6. Exit

Enter your choice: 1
Enter task title: Buy groceries
Enter task description (optional): Milk, bread, eggs
Task added successfully with ID: 1
```

## Development

### Project Structure
```
src/
├── todo_app/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py
│   └── cli/
│       ├── __init__.py
│       └── menu.py
```

### Key Components
- `task.py`: Defines the Task model with validation
- `task_service.py`: Handles all task operations
- `menu.py`: Manages the console interface
- `main.py`: Application entry point

## Testing

To run tests:
```bash
pytest tests/
```

The application includes unit tests for all components and integration tests for the main user flows.

## Limitations

- Data is stored in memory only and will be lost when the application exits
- No file or database persistence
- Single-user application
- Console-based interface only