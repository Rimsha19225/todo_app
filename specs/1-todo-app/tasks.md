# Implementation Tasks: In-Memory Python Console Todo Application

**Feature**: 1-todo-app
**Date**: 2026-01-01
**Status**: Draft
**Spec**: [specs/1-todo-app/spec.md](../specs/1-todo-app/spec.md)
**Plan**: [specs/1-todo-app/plan.md](../specs/1-todo-app/plan.md)

## Dependencies

User stories can be implemented in parallel after foundational setup is complete. User Story 1 (Add Tasks) provides the basic data model needed for other stories. User Stories 6-10 (Search, Filter, Sort, Overdue, Upcoming) can be implemented in parallel after the core CRUD functionality is established.

## Parallel Execution Examples

- User Story 2 (View Tasks) can be developed in parallel with User Story 3 (Update Tasks) after foundational models exist
- User Story 4 (Delete Tasks) and User Story 5 (Mark Complete) can be developed in parallel after foundational models exist
- User Stories 6-10 (Search, Filter, Sort, Overdue, Upcoming) can be developed in parallel after core CRUD functionality exists

## Implementation Strategy

Start with MVP containing User Story 1 (Add Tasks) and User Story 2 (View Tasks) to provide core functionality. Then incrementally add other features including User Stories 3-5 (Update, Delete, Complete) followed by advanced features in User Stories 6-10 (Search, Filter, Sort, Overdue, Upcoming).

---

## Phase 1: Setup

Goal: Initialize project structure and dependencies

- [ ] T001 Create project directory structure per plan.md
- [ ] T002 Initialize Python project with setup files
- [ ] T003 Create source directory structure (src/todo_app/, models/, services/, cli/)

---

## Phase 2: Foundational

Goal: Core models and services that support all user stories

- [x] T004 [P] Create Task model class in src/todo_app/models/task.py
- [x] T005 [P] Create TaskService class in src/todo_app/services/task_service.py
- [x] T006 [P] Implement in-memory storage mechanism for tasks
- [x] T007 [P] Implement ID generation logic for tasks
- [x] T008 [P] Add validation logic for task creation

---

## Phase 3: User Story 1 - Add and Manage Tasks (Priority: P1)

Goal: As a user, I want to add tasks to my todo list so that I can keep track of things I need to do.

**Independent Test**: Can be fully tested by adding a task with a title and verifying it appears in the list, delivering the fundamental value of task management.

- [x] T009 [US1] Implement add_task method in TaskService
- [x] T010 [US1] Add input validation for required title in TaskService
- [x] T011 [US1] Add input validation for optional description in TaskService
- [x] T012 [US1] Create CLI menu option for adding tasks in src/todo_app/cli/menu.py
- [x] T013 [US1] Implement CLI input handling for task creation
- [x] T014 [US1] Add success message display after task creation
- [x] T015 [US1] Create unit tests for task creation functionality

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

Goal: As a user, I want to view all my tasks so that I can see what I need to do.

**Independent Test**: Can be fully tested by adding tasks and then viewing the complete list, delivering the core value of task visibility.

- [x] T016 [US2] Implement get_all_tasks method in TaskService
- [x] T017 [US2] Create CLI menu option for viewing all tasks in src/todo_app/cli/menu.py
- [x] T018 [US2] Implement formatted display of all tasks
- [x] T019 [US2] Handle case where no tasks exist
- [x] T020 [US2] Add display of ID, title, description, and completion status
- [x] T021 [US2] Create unit tests for viewing tasks functionality

---

## Phase 5: User Story 3 - Update Task Details (Priority: P2)

Goal: As a user, I want to update my tasks so that I can modify the information as needed.

**Independent Test**: Can be fully tested by updating a task and verifying the changes are reflected, delivering value in task maintenance.

- [x] T022 [US3] Implement update_task method in TaskService
- [x] T023 [US3] Add validation for valid task ID in TaskService
- [x] T024 [US3] Create CLI menu option for updating tasks in src/todo_app/cli/menu.py
- [x] T025 [US3] Implement input handling for task ID and updates
- [x] T026 [US3] Add error handling for invalid task IDs
- [x] T027 [US3] Create unit tests for task update functionality

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P2)

Goal: As a user, I want to delete tasks so that I can remove items I no longer need.

**Independent Test**: Can be fully tested by deleting a task and verifying it no longer appears in the list, delivering value in task management.

- [x] T028 [US4] Implement delete_task method in TaskService
- [x] T029 [US4] Add validation for valid task ID in TaskService
- [x] T030 [US4] Create CLI menu option for deleting tasks in src/todo_app/cli/menu.py
- [x] T031 [US4] Implement input handling for task ID to delete
- [x] T032 [US4] Add error handling for invalid task IDs
- [x] T033 [US4] Add confirmation message after successful deletion
- [x] T034 [US4] Create unit tests for task deletion functionality

---

## Phase 7: User Story 5 - Mark Tasks Complete/Incomplete (Priority: P1)

Goal: As a user, I want to mark tasks as complete or incomplete so that I can track my progress.

**Independent Test**: Can be fully tested by marking tasks as complete/incomplete and seeing the status change, delivering the value of progress tracking.

- [x] T035 [US5] Implement mark_task_complete method in TaskService
- [x] T036 [US5] Implement mark_task_incomplete method in TaskService
- [x] T037 [US5] Create CLI menu option for marking tasks complete/incomplete in src/todo_app/cli/menu.py
- [x] T038 [US5] Implement input handling for task ID and completion status
- [x] T039 [US5] Add validation for valid task ID
- [x] T040 [US5] Add error handling for invalid task IDs
- [x] T041 [US5] Create unit tests for task completion functionality

---

## Phase 8: CLI Integration and Menu System

Goal: Create the main console menu interface that integrates all functionality

- [x] T042 Create main menu loop in src/todo_app/main.py
- [x] T043 Implement numbered menu options for all user stories
- [x] T044 Add error handling for invalid menu selections
- [x] T045 Create clear success and error messages for all operations
- [x] T046 Add graceful handling of invalid task IDs
- [x] T047 Implement application exit functionality

---

## Phase 9: Testing and Quality Assurance

Goal: Ensure all functionality works correctly and meets requirements

- [x] T048 Create integration tests for CLI interface
- [x] T049 Create tests for all acceptance scenarios from spec.md
- [x] T050 Create tests for edge cases identified in spec.md
- [x] T051 Add tests for error handling scenarios
- [x] T052 Run all tests to verify functionality

---

## Phase 10: User Story 6 - Search Tasks (Priority: P2)

Goal: As a user, I want to search for tasks by keyword so that I can quickly find specific tasks.

**Independent Test**: Can be fully tested by adding tasks with different titles/descriptions and searching for specific keywords, delivering value in task discovery.

- [x] T059 [US6] Implement search_tasks method in TaskService
- [x] T060 [US6] Add search functionality that looks for keywords in title and description
- [x] T061 [US6] Create CLI menu option for searching tasks in src/todo_app/cli/menu.py
- [x] T062 [US6] Implement input handling for search keyword
- [x] T063 [US6] Add case-insensitive search functionality
- [x] T064 [US6] Create unit tests for search functionality

---
## Phase 11: User Story 7 - Filter Tasks (Priority: P2)

Goal: As a user, I want to filter tasks by various criteria so that I can view only the tasks that match my current needs.

**Independent Test**: Can be fully tested by filtering tasks by different criteria and verifying the correct tasks are displayed, delivering value in task organization.

- [x] T065 [US7] Implement filter_tasks method in TaskService
- [x] T066 [US7] Add filtering by status, priority, due date, and category
- [x] T067 [US7] Create CLI menu option for filtering tasks in src/todo_app/cli/menu.py
- [x] T068 [US7] Implement input handling for filter criteria
- [x] T069 [US7] Add support for multiple filter criteria
- [x] T070 [US7] Create unit tests for filter functionality

---
## Phase 12: User Story 8 - Sort Tasks (Priority: P2)

Goal: As a user, I want to sort tasks by various criteria so that I can view them in a preferred order.

**Independent Test**: Can be fully tested by sorting tasks by different criteria and verifying they are displayed in the correct order, delivering value in task organization.

- [x] T071 [US8] Implement sort_tasks method in TaskService
- [x] T072 [US8] Add sorting by title, priority, due date, category, and status
- [x] T073 [US8] Create CLI menu option for sorting tasks in src/todo_app/cli/menu.py
- [x] T074 [US8] Implement input handling for sort criteria and order
- [x] T075 [US8] Add ascending/descending sort options
- [x] T076 [US8] Create unit tests for sort functionality

---
## Phase 13: User Story 9 - View Overdue Tasks (Priority: P2)

Goal: As a user, I want to view all overdue tasks so that I can identify tasks that are past their due date.

**Independent Test**: Can be fully tested by creating tasks with past due dates and viewing the overdue list, delivering value in task tracking.

- [x] T077 [US9] Implement get_overdue_tasks method in TaskService
- [x] T078 [US9] Add logic to identify tasks with past due dates that are not completed
- [x] T079 [US9] Create CLI menu option for viewing overdue tasks in src/todo_app/cli/menu.py
- [x] T080 [US9] Implement display of overdue tasks
- [x] T081 [US9] Create unit tests for overdue task functionality

---
## Phase 14: User Story 10 - View Upcoming Tasks (Priority: P2)

Goal: As a user, I want to view upcoming tasks so that I can plan for tasks that will be due soon.

**Independent Test**: Can be fully tested by creating tasks with future due dates and viewing the upcoming list, delivering value in task planning.

- [x] T082 [US10] Implement get_upcoming_tasks method in TaskService
- [x] T083 [US10] Add logic to identify tasks due within a specified number of days
- [x] T084 [US10] Create CLI menu option for viewing upcoming tasks in src/todo_app/cli/menu.py
- [x] T085 [US10] Implement input handling for number of days to look ahead
- [x] T086 [US10] Create unit tests for upcoming task functionality

---
## Phase 15: Recurring Tasks and Reminders

Goal: Implement recurring task functionality and additional reminder features.

- [x] T087 Implement recurring task logic in mark_task_complete method
- [x] T088 Implement calculate_next_due_date helper method
- [x] T089 Add support for daily, weekly, and monthly recurring patterns
- [x] T090 Implement get_due_tasks_for_date method
- [x] T091 Create unit tests for recurring and reminder functionality
- [x] T092 Update Task model to support all new attributes (priority, due date, recurring pattern, category)

---
## Phase 16: CLI Menu Updates

Goal: Update CLI menu to include all new functionality.

- [x] T093 Update menu display to show all 11 options (including search, filter, sort, overdue, upcoming)
- [x] T094 Implement handlers for all new menu options in src/todo_app/cli/menu.py
- [x] T095 Update add task CLI to include priority, due date, recurring pattern, and category inputs
- [x] T096 Update update task CLI to include all new field options
- [x] T097 Add input validation for all new features in CLI

---
## Phase 17: Testing and Quality Assurance

Goal: Ensure all new functionality works correctly and meets requirements

- [x] T098 Create integration tests for all new features
- [x] T099 Update existing tests to handle new task attributes
- [x] T100 Create tests for all new acceptance scenarios from spec.md
- [x] T101 Create tests for new edge cases identified in spec.md
- [x] T102 Run all tests to verify new functionality works correctly

---
## Phase 18: Polish & Cross-Cutting Concerns

Goal: Final touches and cross-cutting concerns

- [x] T103 Add input validation for new fields (priority, due date, recurring pattern, category)
- [x] T104 Add documentation to all new public methods
- [x] T105 Ensure consistent error message formatting for new features
- [x] T106 Add input sanitization for new features
- [x] T107 Update README with new features and usage instructions
- [x] T108 Verify all new requirements from spec.md are met