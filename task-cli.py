import sys
import json
from datetime import datetime

def main():
    try:
        command = sys.argv[1]
        with open("storage.json",'r') as file:
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
            with open("storage.json", "w") as file:
                json.dump(tasks, file, indent=4)
            print (f'Task added successfully (ID: {id})')

        elif command == 'update':
            if len(sys.argv) != 4:
                raise ValueError("Missing task id and/or change string")
            task_id = int(sys.argv[2])
            found = False
            for tsk in tasks:
                if tsk['ID'] == task_id:
                    tsk["description"] = sys.argv[3]
                    tsk["UpdatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                    found = True
                    break

            if not found:
                raise ValueError(f"Task with ID {task_id}")
            
            with open("storage.json", "w") as file:
                json.dump(tasks, file, indent=4)

        elif command == 'delete':
            if len(sys.argv) != 3:
                raise ValueError("Missing task id")
            task_id = int(sys.argv[2])
            found = False
            for tsk in tasks:
                if tsk['ID'] == task_id:
                    found = True
                    tasks.remove(tsk)
                    break
                
            if not found:
                raise ValueError(f"Task with ID {task_id} not found")
            
            with open("storage.json", "w") as file:
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
            
            with open("storage.json", "w") as file:
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
            
            with open("storage.json", "w") as file:
                json.dump(tasks, file, indent=4)
        elif command == 'list':
            print('-'* 35)
            print('| Task |  description  |  status  |')
            print('-'* 35)
            if len(sys.argv) == 2:
                for tsk in tasks:
                    print(f"   {tsk['ID']}.  | {tsk['description']} | {tsk['status']}")
                sys.exit(0)

            if sys.argv[2] == 'done':
                for tsk in tasks:
                    if tsk["status"] == 'done':
                        print(f"   {tsk['ID']}.  | {tsk['description']} | {tsk['status']}")
                        continue
                sys.exit(0)
            elif sys.argv[2] == 'todo':
                for tsk in tasks:
                    if tsk["status"] == 'todo':
                        print(f"   {tsk['ID']}.  | {tsk['description']} | {tsk['status']}")
                        continue
                sys.exit(0)
            elif sys.argv[2] == 'in-progress':
                for tsk in tasks:
                    if tsk["status"] == 'in progress':
                        print(f"   {tsk['ID']}.  | {tsk['description']} | {tsk['status']}")
                        continue
                sys.exit(0)
            else:
                return 'command not found or bad usage'
    except IndexError:
        print('Usage: task-cli command "task"')
        sys.exit(1)
    except ValueError as e:
        print(e)
        sys.exit(1)

main()