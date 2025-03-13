#!/usr/bin/env python3
import os
import json
import datetime
from colorama import Fore, Style, init

# initialize colorama
init(autoreset=True)

# priority colors
PRIORITY_COLORS = {
    "high": Fore.RED,
    "medium": Fore.YELLOW,
    "low": Fore.GREEN
}

class TodoList:
    def __init__(self):
        self.tasks = []
        self.filename = "tasks.json"
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    self.tasks = json.load(f)
            except json.JSONDecodeError:
                print("Error loading tasks file. Starting with empty list")
                self.tasks = []
        else:
            self.tasks = []

    def save_tasks(self):
        with open(self.filename, 'w') as f:
            json.dump(self.tasks, f, indent=2)
        print(f"Tasks saved to {self.filename}")

    def add_task(self, name, priority="medium"):
        if priority not in PRIORITY_COLORS:
            print(f"Invalid priority. Choose from: {','.join(PRIORITY_COLORS.keys())}")
            return
        
        task = {
            "id": len(self.tasks) + 1,
            "name": name,
            "priority": priority,
            "done": False,
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.tasks.append(task)
        self.sort_tasks()
        print(f"Task added: {name}")

    def delete_task(self, task_id):
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                deleted_task = self.tasks.pop(i)
                print(f"Deleted task: {deleted_task['name']}")
                return
            print(f"No task found with ID {task_id}")
    
    def update_task(self, task_id, name=None, priority=None):
        for task in self.tasks:
            if task["id"] == task_id:
                if name:
                    task["name"] = name
                if priority:
                    if priority in PRIORITY_COLORS:
                        task["priority"] = priority
                    else:
                        print(f"Invalid priorty. Choose from: {','.join(PRIORITY_COLORS.keys())}")
                        return
                print(f"Updated task {task_id}")
                self.sort_tasks()
                return
        print(f"No task found with ID {task_id}")

    def mark_done(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                task["done"] = not task["done"]
                status = "completed" if task["done"] else "pending"
                print(f"Marked task {task_id} as {status}")
                self.sort_tasks()
                return
        print(f"No task found with ID {task_id}")
    
    def sort_tasks(self):
        # define priority order
        priority_order = {"high": 0, "medium": 1, "low": 2}

        # sort by done status first, then by priority
        self.tasks.sort(key=lambda x: (x["done"], priority_order.get(x["priority"], 999)))

    def list_tasks(self):
        if not self.tasks:
            print("No tasks found.")
            return
        
        print("\nYour To-Do List:")
        print("=" * 80)
        print(f"{'ID':<5}{'STATUS':<10}{'NAME':<10}{'PRIORITY':<50}")
        print("-" * 80)

        for task in self.tasks:
            status = "✓" if task["done"] else "□"
            color = PRIORITY_COLORS.get(task["priority"], "")
            print(f"{task['id']:<5}{status:<10}{color}{task['name']:<10}{task['priority']:<50}{Style.RESET_ALL}")
            print("=" * 80)
    
    # save file as .md format
    def export_to_markdown(self):
        if not self.tasks:
            print("No tasks to export.")
            return
        
        filename = f"todo_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        with open(filename, 'w') as f:
            f.write("# Todo List\n\n")
            f.write(f"Exported on : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n")

            # write pending tasks
            f.write("## Pending Tasks\n\n")
            for task in self.tasks:
                if not task["done"]:
                    checkbox = "- [ ] "
                    priority_tag = f"[!{task['priority']}] " if task['priority'] in PRIORITY_COLORS else ""
                    f.write(f"{checkbox}{priority_tag}{task['name']}\n")
            
            # write completed tasks
            f.write("\n## Completed Tasks\n\n")
            for task in self.tasks:
                if task["done"]:
                    checkbox = ['- [x] ']
                    priority_tag = f"[!{task['priority']}] " if task['priority'] in PRIORITY_COLORS else ""
                    f.write(f"{checkbox}{priority_tag}{task['name']}\n")
            
        print(f"Tasks exported to {filename}")
        return filename
    
def display_menu():
    print("\nTo-Do List")
    print("1. Add Task")
    print("2. Mark Task")
    print("3. List Tasks")
    print("4. Delete Task")
    print("5. Update Task")
    print("6. Export Tasks")
    print("7. Exit")
    return input("Select an option: ")

def main():
    todo_list = TodoList()

    while True:
        choice = display_menu()

        priority_map = {
            '1': 'high',
            '2': 'medium',
            '3': 'low'
        }

        if choice == '1':
            name = input("Enter task name: ")
            priority_input = int(input("Enter priority (1: high | 2: medium | 3: low): "))
            priority = priority_map.get(priority_input)
            if not priority:
                priority = "medium"
            todo_list.add_task(name, priority)
        elif choice == '2':
            try:
                task_id = int(input("Enter task number to mark as done/undone: "))
                todo_list.mark_done(task_id)
            except ValueError:
                print("Please enter a valid task number.")
        elif choice == '3':
            todo_list.list_tasks()
        elif choice == '4':
            try:
                task_id = int(input("Enter task number to delete: "))
                todo_list.delete_task(task_id)
            except ValueError:
                print("Please enter a valid task number.")
        elif choice == '5':
            try:
                task_id = int(input("Enter task number to update: "))
                name = input("Enter new name: ")
                priority = int(input("Enter a new priority (1: high | 2: medium | 3: low): "))
                priority_input = int(input("Enter priority (1: high | 2: medium 3: low): "))
                priority = priority_map.get(priority_input)
                todo_list.update_task(task_id, name, priority)
            except ValueError:
                print("Please enter a valid task number.")
        elif choice == '6':
            todo_list.export_to_markdown()
        elif choice == '7':
            todo_list.save_tasks()
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again")

if __name__ == "__main__":
    main()   
