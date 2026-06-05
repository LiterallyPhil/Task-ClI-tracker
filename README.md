# Task CLI

A simple command-line task tracker written in Python. Tasks are stored locally in a `storage.json` file.

## Features

* Add new tasks
* Update task descriptions
* Delete tasks
* Mark tasks as in progress
* Mark tasks as done
* List all tasks
* Filter tasks by status
* Generate unique task IDs safely

## Requirements

* Python 3
* A `storage.json` file in the same directory as the script

Create `storage.json` before running the program:

```json
[]
```

## Usage

```bash
python task_cli.py <command> [arguments]
```

## Commands

### Add a task

```bash
python task_cli.py add "Buy groceries"
```

Example output:

```bash
Task added successfully (ID: 1)
```

### Update a task

```bash
python task_cli.py update 1 "Buy groceries and cook dinner"
```

### Delete a task

```bash
python task_cli.py delete 1
```

### Mark a task as in progress

```bash
python task_cli.py mark-in-progress 1
```

### Mark a task as done

```bash
python task_cli.py mark-done 1
```

### List all tasks

```bash
python task_cli.py list
```

### List completed tasks

```bash
python task_cli.py list done
```

### List todo tasks

```bash
python task_cli.py list todo
```

### List in-progress tasks

```bash
python task_cli.py list in-progress
```

## Task Format

Each task is stored as an object inside `storage.json`:

```json
{
    "ID": 1,
    "description": "Buy groceries",
    "status": "todo",
    "createdAt": "2026-06-05 14:30",
    "UpdatedAt": "2026-06-05 14:30"
}
```

## ID Generation

Task IDs are generated using the highest existing task ID plus one:

```python
id = max((task["ID"] for task in tasks), default=0) + 1
```

This makes sure new task IDs stay unique, even after tasks are deleted.

For example, if `storage.json` contains:

```json
[
    { "ID": 1, "description": "First task" },
    { "ID": 3, "description": "Third task" }
]
```

The next task will receive:

```text
ID: 4
```

not:

```text
ID: 3
```

## Notes

* The program expects `storage.json` to already exist.
* Task statuses are stored as `todo`, `in progress`, or `done`.
* Use quotes around task descriptions that contain spaces.
* IDs are not reused after deletion, which helps avoid confusion.
