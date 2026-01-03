# In-Memory Python Console Todo Application

A simple console-based todo application implemented in Python with in-memory storage. This application allows users to manage their tasks through a menu-driven interface.

## Features

- Add tasks with titles, descriptions, priority levels, due dates, recurring patterns, and categories
- View all tasks with their completion status, priority, due dates, recurring patterns, and categories
- Update existing tasks with all attributes
- Delete tasks
- Mark tasks as complete or incomplete (with recurring task support)
- Search tasks by keyword in title or description
- Filter tasks by status, priority, due date, and category
- Sort tasks by title, priority, due date, category, or status
- View overdue tasks (tasks past their due date that are not completed)
- View upcoming tasks (tasks due within a specified number of days)
- View tasks due on a specific date
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
   - 6. Search Tasks
   - 7. Filter Tasks
   - 8. Sort Tasks
   - 9. View Overdue Tasks
   - 10. View Upcoming Tasks
   - 11. Exit

3. Select an option by entering the corresponding number
4. Follow the prompts to perform the desired action

### Adding a Task
- Enter option 1
- Provide a title (required)
- Optionally provide a description
- Select priority level (high, medium, low)
- Optionally enter due date (YYYY-MM-DD format)
- Select recurring pattern (daily, weekly, monthly, none)
- Select category (work, home, or other)
- The task will be added with a unique ID

### Viewing Tasks
- Enter option 2
- All tasks will be displayed with their ID, title, description, completion status, priority, due date, recurring pattern, and category

### Updating a Task
- Enter option 3
- Provide the task ID you want to update
- Enter new values for title, description, priority, due date, recurring pattern, and category when prompted

### Deleting a Task
- Enter option 4
- Provide the task ID you want to delete

### Marking Tasks Complete/Incomplete
- Enter option 5
- Provide the task ID
- Choose whether to mark it as complete or incomplete
- For recurring tasks, a new instance will be created with the next due date when marked complete

### Searching Tasks
- Enter option 6
- Enter a keyword to search in task titles or descriptions
- All matching tasks will be displayed

### Filtering Tasks
- Enter option 7
- Specify filter criteria (status, priority, due date, category)
- All tasks matching the criteria will be displayed

### Sorting Tasks
- Enter option 8
- Choose the sorting criteria (title, priority, due date, category, status)
- Choose ascending or descending order
- Tasks will be displayed in the sorted order

### Viewing Overdue Tasks
- Enter option 9
- All tasks past their due date that are not completed will be displayed

### Viewing Upcoming Tasks
- Enter option 10
- Specify the number of days to look ahead (default is 7)
- All tasks due within the specified period that are not completed will be displayed

### Exiting the Application
- Enter option 11 to exit the application

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

- **Models**: Define the data structures (Task model with title, description, completion status, priority, due date, recurring pattern, and category)
- **Services**: Handle the business logic (TaskService with CRUD operations, search, filter, sort, recurring tasks, and reminder functionality)
- **CLI**: Handle the user interface (Menu class with all user interaction features)

## Limitations

- Data is stored in memory only and will be lost when the application exits
- No file or database persistence
- Single-user application
- Console-based interface only
- No advanced scheduling beyond daily, weekly, and monthly recurring patterns

## Development

The project includes comprehensive unit and integration tests covering all functionality including CRUD operations, search, filter, sort, recurring tasks, and reminder features to ensure functionality meets the specified requirements.
