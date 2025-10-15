import json
import os

FILE_NAME = "tasks.json"

# ✅ Load tasks from file if exists
def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []

# 💾 Save tasks to file
def save_tasks(tasks):
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)

# 🧩 Display menu
def show_menu():
    print("\n====== TO-DO LIST APP ======")
    print("1. View All Tasks")
    print("2. View Pending Tasks")
    print("3. View Completed Tasks")
    print("4. Add Task")
    print("5. Mark Task as Completed")
    print("6. Remove Task")
    print("7. Exit")

# 📋 View tasks
def view_tasks(tasks, filter_by=None):
    if not tasks:
        print("\nNo tasks found.")
        return

    filtered_tasks = tasks
    if filter_by == "pending":
        filtered_tasks = [t for t in tasks if not t["completed"]]
    elif filter_by == "completed":
        filtered_tasks = [t for t in tasks if t["completed"]]

    if not filtered_tasks:
        print(f"\nNo {filter_by or 'tasks'} found.")
        return

    print("\nYour Tasks:")
    for i, task in enumerate(filtered_tasks, 1):
        status = "✔" if task["completed"] else "❌"
        print(f"{i}. {task['title']} [{status}]")

# ➕ Add new task
def add_task(tasks):
    title = input("Enter task title: ").strip()
    if title:
        task = {"title": title, "completed": False}
        tasks.append(task)
        save_tasks(tasks)
        print(f"✅ '{title}' added successfully!")
    else:
        print("Task title cannot be empty.")

# ✅ Mark a task as completed
def mark_completed(tasks):
    view_tasks(tasks, filter_by="pending")
    if not tasks:
        return
    try:
        index = int(input("Enter the number of the task to complete: ")) - 1
        pending_tasks = [t for t in tasks if not t["completed"]]
        if 0 <= index < len(pending_tasks):
            pending_tasks[index]["completed"] = True
            save_tasks(tasks)
            print(f"🎉 '{pending_tasks[index]['title']}' marked as completed!")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

# 🗑 Remove a task
def remove_task(tasks):
    view_tasks(tasks)
    if not tasks:
        return
    try:
        index = int(input("Enter the number of the task to remove: ")) - 1
        if 0 <= index < len(tasks):
            removed = tasks.pop(index)
            save_tasks(tasks)
            print(f"🗑 '{removed['title']}' removed.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

# 🚀 Main program
def main():
    tasks = load_tasks()
    while True:
        show_menu()
        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            view_tasks(tasks)
        elif choice == "2":
            view_tasks(tasks, filter_by="pending")
        elif choice == "3":
            view_tasks(tasks, filter_by="completed")
        elif choice == "4":
            add_task(tasks)
        elif choice == "5":
            mark_completed(tasks)
        elif choice == "6":
            remove_task(tasks)
        elif choice == "7":
            print("👋 Goodbye! Your tasks are saved.")
            break
        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    main()
