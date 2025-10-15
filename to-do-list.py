import tkinter as tk
from tkinter import messagebox
import json
import os

FILE_NAME = "tasks.json"

# ----------------- File Functions -----------------
def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []

def save_tasks(tasks):
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)

# ----------------- Main App -----------------
class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📝 To-Do List App")
        self.root.geometry("400x500")
        self.root.config(bg="#f5f5f5")

        self.tasks = load_tasks()

        # Title
        tk.Label(root, text="My Tasks", font=("Helvetica", 18, "bold"), bg="#f5f5f5").pack(pady=10)

        # Listbox
        self.listbox = tk.Listbox(
            root,
            width=40,
            height=15,
            selectmode=tk.SINGLE,
            font=("Helvetica", 12),
            bg="#fff",
            fg="#333",
            selectbackground="#a6e3a1",
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
        )
        self.listbox.pack(pady=10)

        # Load existing tasks
        self.load_listbox()

        # Entry field
        self.task_entry = tk.Entry(root, font=("Helvetica", 12), width=25, bd=1, relief="solid")
        self.task_entry.pack(pady=5)

        # Buttons Frame
        button_frame = tk.Frame(root, bg="#f5f5f5")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Add", command=self.add_task, width=8, bg="#4CAF50", fg="white", font=("Helvetica", 10)).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Complete", command=self.mark_complete, width=8, bg="#2196F3", fg="white", font=("Helvetica", 10)).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Delete", command=self.delete_task, width=8, bg="#f44336", fg="white", font=("Helvetica", 10)).grid(row=0, column=2, padx=5)

    # ----------------- Functions -----------------
    def load_listbox(self):
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            display_text = f"✔ {task['title']}" if task["completed"] else f"❌ {task['title']}"
            self.listbox.insert(tk.END, display_text)

    def add_task(self):
        title = self.task_entry.get().strip()
        if title:
            task = {"title": title, "completed": False}
            self.tasks.append(task)
            save_tasks(self.tasks)
            self.load_listbox()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a task.")

    def mark_complete(self):
        try:
            index = self.listbox.curselection()[0]
            self.tasks[index]["completed"] = True
            save_tasks(self.tasks)
            self.load_listbox()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to complete.")

    def delete_task(self):
        try:
            index = self.listbox.curselection()[0]
            removed_task = self.tasks.pop(index)
            save_tasks(self.tasks)
            self.load_listbox()
            messagebox.showinfo("Deleted", f"Task '{removed_task['title']}' deleted.")
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

# ----------------- Run App -----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
