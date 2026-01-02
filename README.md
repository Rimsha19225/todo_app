# In-Memory Python Console Todo Application

A simple console-based todo application implemented in Python with in-memory storage. This application allows users to manage their tasks through a menu-driven interface.

## Features

- Add tasks with titles, descriptions, priority levels, due dates, and recurring patterns
- View all tasks with their completion status, priority, due dates, and recurring patterns
- Update existing tasks with all attributes
- Delete tasks
- Mark tasks as complete or incomplete
- In-memory storage (data is lost when the application exits)

## Requirements

- Python 3.8 or higher

## Installation

1. Clone or download the repository
2. Navigate to the project directory
3. Ensure Python 3.8+ is installed on your system

## Usage

To run the application:

```bash
python -m src.todo_app.main
```

## How to Use

1. Run the application using the command above
2. You will see a menu with the following options:
   - 1. Add Task
   - 2. View All Tasks
   - 3. Update Task
   - 4. Delete Task
   - 5. Mark Task Complete/Incomplete
   - 6. Exit

3. Select an option by entering the corresponding number
4. Follow the prompts to perform the desired action

### Adding a Task
- Enter option 1
- Provide a title (required)
- Optionally provide a description
- Select priority level (high, medium, low)
- Optionally enter due date (YYYY-MM-DD format)
- Select recurring pattern (daily, weekly, monthly, none)
- The task will be added with a unique ID

### Viewing Tasks
- Enter option 2
- All tasks will be displayed with their ID, title, description, completion status, priority, due date, and recurring pattern

### Updating a Task
- Enter option 3
- Provide the task ID you want to update
- Enter new values for title, description, priority, due date, and recurring pattern when prompted

### Deleting a Task
- Enter option 4
- Provide the task ID you want to delete

### Marking Tasks Complete/Incomplete
- Enter option 5
- Provide the task ID
- Choose whether to mark it as complete or incomplete

### Exiting the Application
- Enter option 6 to exit the application

## Project Structure

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
tests/
├── unit/
│   ├── test_task.py
│   └── test_task_service.py
└── integration/
    └── test_cli.py
```

## Running Tests

To run the tests:

```bash
pip install pytest
pytest tests/
```

## Architecture

The application follows a clean architecture pattern:

- **Models**: Define the data structures (Task model)
- **Services**: Handle the business logic (TaskService)
- **CLI**: Handle the user interface (Menu class)

## Limitations

- Data is stored in memory only and will be lost when the application exits
- No file or database persistence
- Single-user application
- Console-based interface only

## Development

The project includes comprehensive unit and integration tests to ensure functionality meets the specified requirements.# todo_app
