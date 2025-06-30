import json
from datetime import datetime
import re

FILENAME = "tasks.json"

def load_tasks():
    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)

def valid_date(date_str):
    return re.match(r"^\d{4}/\d{2}/\d{2}$", date_str) is not None

def display_tasks(tasks):
    if not tasks:
        print("No tasks available.")
        return
    for i, task in enumerate(tasks, 1):
        status = "✅" if task.get("done") else "❌"
        print(f"{i}. {task['name']} (Due: {task['deadline']}) [{task['category']}] {status}")

def main():
    tasks = load_tasks()
    print("Welcome to the To-Do List Application!")
    
    while True:
        print("\n===== Menu =====")
        print("1. Show Tasks")
        print("2. Add Task")
        print("3. Delete Task")
        print("4. Exit")
        choice = input("Please select an option (1-4): ")

        if choice == "1":
            display_tasks(tasks)
        elif choice == "2":
            new_task_name = input("Enter the task name: ")
            while True:
                new_task_deadline = input("Enter the task deadline (format: YYYY/MM/DD): ")
                if valid_date(new_task_deadline):
                    break
                else:
                    print("Invalid date format, please try again (format: YYYY/MM/DD).")
            task_category = input("Enter the task category: ")
            task = {
                "name": new_task_name,
                "deadline": new_task_deadline,
                "category": task_category,
                "done": False
            }
            tasks.append(task)
            save_tasks(tasks)
            print(f"Task '{new_task_name}' has been added.")
        elif choice == "3":
            display_tasks(tasks)
            try:
                task_id = int(input("Enter the task number to delete: ")) - 1
                if 0 <= task_id < len(tasks):
                    removed_task = tasks.pop(task_id)
                    save_tasks(tasks)
                    print(f"Task '{removed_task['name']}' has been deleted.")
                else:
                    print("Invalid task number.")
            except ValueError:
                print("Please enter a valid number.")
        elif choice == "4":
            print("Thank you for using the To-Do List Application! Goodbye!")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()