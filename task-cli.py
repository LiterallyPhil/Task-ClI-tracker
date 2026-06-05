#!/usr/bin/env python3

import sys
import json
from datetime import datetime
from pathlib import Path


def display_tasks(tasks):
    if not tasks:
        print('No tasks found.')
        return
    
    headers = ["ID","Description", "Status"]

    rows = []

    for task in tasks:
        row = [str(task["ID"]), task["description"],task["status"] ]
        rows.append(row)

    
    col_widths = []
    
    for i in range(len(headers)):
        col_width = max(len(headers[i]), max(len(row[i])for row in rows))
        col_widths.append(col_width)
    
    separator = "+-" + "-+-".join('-' * width for width in col_widths) + "-+"

    print(
        "| "
        + " | ".join(headers[i].ljust(col_widths[i]) for i in range(len(headers)))
        + " |"
    )
    print(separator)

    for row in rows:
        print(
            "| "
            + " | ".join(row[i].ljust(col_widths[i]) for i in range(len(row)))
            + " |"
        )

    print(separator)





def main():
    try:
        STORAGE_FILE = Path(__file__).parent / "task_cli_storage.json"

        if not STORAGE_FILE.exists():
            STORAGE_FILE.write_text("[]")
        command = sys.argv[1]
        with open(STORAGE_FILE,'r') as file:
            tasks = json.load(file)
            id = max((task["ID"] for task in tasks), default=0) + 1
        if command == 'add':
            task ={
                    "ID": id,
                    "description": sys.argv[2],
                    "status": 'todo',
                    "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "UpdatedAt": datetime.now().strftime("%Y-%m-%d %H:%M")
                   }
            tasks.append(task)
            with open(STORAGE_FILE, "w") as file:
                json.dump(tasks, file, indent=4)
            print (f'Task added successfully (ID: {id})')

        elif command == 'update':
            if len(sys.argv) != 4:
                raise ValueError("Missing task id and/or change string")
            task_id = int(sys.argv[2])
            found = False
            for tsk in tasks:
                if tsk['ID'] == task_id:
                    display_tasks([tsk])
                    tsk["description"] = sys.argv[3]
                    tsk["UpdatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                    print("changed to->")
                    display_tasks([tsk])
                    found = True
                    break

            if not found:
                raise ValueError(f"Task with ID {task_id}")
            
            with open(STORAGE_FILE, "w") as file:
                json.dump(tasks, file, indent=4)

        elif command == 'delete':
            if len(sys.argv) != 3:
                raise ValueError("Missing task id")
            task_id = int(sys.argv[2])
            found = False
            for tsk in tasks:
                if tsk['ID'] == task_id:
                    found = True
                    display_tasks([tsk])
                    print('deleted successfully')
                    tasks.remove(tsk)
                    break
                
            if not found:
                raise ValueError(f"Task with ID {task_id} not found")
            with open(STORAGE_FILE, "w") as file:
                json.dump(tasks, file, indent=4)
        elif command == 'mark-in-progress':
            if len(sys.argv) != 3:
                raise ValueError("Missing task id")
            task_id = int(sys.argv[2])
            found = False
            for tsk in tasks:
                if tsk['ID'] == task_id:
                    found = True
                    tsk["status"] = "in progress"
                    break
                
            if not found:
                raise ValueError(f"Task with ID {task_id} not found")
            
            with open(STORAGE_FILE, "w") as file:
                json.dump(tasks, file, indent=4)
        elif command == 'mark-done':
            if len(sys.argv) != 3:
                raise ValueError("Missing task id")
            
            task_id = int(sys.argv[2])
            found = False
            for tsk in tasks:
                if tsk['ID'] == task_id:
                    found = True
                    tsk["status"] = "done"
                    break
                
            if not found:
                raise ValueError(f"Task with ID {task_id} not found")
            
            with open(STORAGE_FILE, "w") as file:
                json.dump(tasks, file, indent=4)
        elif command == 'list':
            if len(sys.argv) == 2:
                display_tasks(tasks)
                return
           
            elif sys.argv[2] == 'done':
                done_tasks = []
                for tsk in tasks:
                    if tsk["status"] == 'done':
                        done_tasks.append(tsk)
                display_tasks(done_tasks)

            elif sys.argv[2] == 'todo':
                todo_tasks = []
                for tsk in tasks:
                    if tsk["status"] == 'todo':
                        todo_tasks.append(tsk)
                display_tasks(todo_tasks)
            
            elif sys.argv[2] == 'in-progress':
                ongoing_tasks = []
                for tsk in tasks:
                    if tsk["status"] == 'in progress':
                        ongoing_tasks.append(tsk)
                display_tasks (ongoing_tasks)
                
            else:
                return 'command not found or bad usage'
    except IndexError:
        print('Usage: task-cli command "task"')
        sys.exit(1)
    except ValueError as e:
        print(e)
        sys.exit(1)

main()