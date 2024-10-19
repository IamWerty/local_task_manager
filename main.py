import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os
import webbrowser

# Створення директорії для завдань, якщо не існує
if not os.path.exists("./tasks"):
    os.makedirs("./tasks")

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        self.root.config(bg="#2e2e2e")

        self.selected_task_name = None
        self.task_data = None

        # Лівий фрейм для списку завдань
        self.left_frame = tk.Frame(self.root, width=200, bg="#3a3a3a")
        self.left_frame.pack(side="left", fill="y")

        # Кнопка фільтрації
        self.filter_button = tk.Button(self.left_frame, text="Фільтрація", command=self.toggle_filters, bg="#4a4a4a", fg="white")
        self.filter_button.pack(pady=10)

        self.filter_status_button = tk.Button(self.left_frame, text="За статусом", command=lambda: self.filter_tasks("status"), bg="#4a4a4a", fg="white")
        self.filter_priority_button = tk.Button(self.left_frame, text="За пріоритетом", command=lambda: self.filter_tasks("priority"), bg="#4a4a4a", fg="white")

        self.task_listbox = tk.Listbox(self.left_frame, bg="#3a3a3a", fg="white")
        self.task_listbox.pack(fill="both", expand=True)
        self.task_listbox.bind("<<ListboxSelect>>", self.on_task_select)

        self.right_frame = tk.Frame(self.root, bg="#2e2e2e")
        self.right_frame.pack(side="right", fill="both", expand=True)

        self.task_title_label = tk.Label(self.right_frame, text="Назва:", bg="#2e2e2e", fg="white")
        self.task_title_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        self.task_title_value = tk.Label(self.right_frame, text="", bg="#2e2e2e", fg="white")
        self.task_title_value.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        self.task_description_label = tk.Label(self.right_frame, text="Опис:", bg="#2e2e2e", fg="white")
        self.task_description_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        self.task_description_value = tk.Label(self.right_frame, text="", bg="#2e2e2e", fg="white")
        self.task_description_value.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        self.task_priority_label = tk.Label(self.right_frame, text="Пріоритет:", bg="#2e2e2e", fg="white")
        self.task_priority_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        self.task_priority_value = tk.Label(self.right_frame, text="", bg="#2e2e2e", fg="white")
        self.task_priority_value.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        self.task_status_label = tk.Label(self.right_frame, text="Статус:", bg="#2e2e2e", fg="white")
        self.task_status_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)

        self.task_status_value = tk.Label(self.right_frame, text="", bg="#2e2e2e", fg="white")
        self.task_status_value.grid(row=3, column=1, sticky="w", padx=10, pady=5)

        self.task_open_button = tk.Button(self.right_frame, text="Open", command=self.open_task, bg="#4a4a4a", fg="white")
        self.task_open_button.grid(row=4, column=1, sticky="w", padx=10, pady=5)

        self.edit_button = tk.Button(self.right_frame, text="Редагувати", command=self.edit_task, bg="#4a4a4a", fg="white")
        self.edit_button.grid(row=5, column=1, sticky="w", padx=10, pady=5)

        self.delete_button = tk.Button(self.right_frame, text="Видалити", command=self.delete_task, bg="#4a4a4a", fg="white")
        self.delete_button.grid(row=6, column=1, sticky="w", padx=10, pady=5)

        self.add_task_button = tk.Button(self.right_frame, text="Додати завдання", command=self.add_task, bg="#4a4a4a", fg="white")
        self.add_task_button.grid(row=0, column=2, padx=10, pady=5)

        self.load_tasks()

    def toggle_filters(self):
        if self.filter_status_button.winfo_ismapped():
            self.filter_status_button.pack_forget()
            self.filter_priority_button.pack_forget()
        else:
            self.filter_status_button.pack(pady=5)
            self.filter_priority_button.pack(pady=5)

    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        for filename in os.listdir("./tasks"):
            if filename.endswith(".json"):
                with open(f"./tasks/{filename}", "r", encoding="utf-8") as file:
                    task = json.load(file)
                    # Додати елемент з кольором в залежності від пріоритету
                    if task["priority"] == "Високий":
                        self.task_listbox.insert(tk.END, task["title"])
                        self.task_listbox.itemconfig(tk.END, {'bg': 'red'})  # Червоний для високого пріоритету
                    elif task["priority"] == "Середній":
                        self.task_listbox.insert(tk.END, task["title"])
                        self.task_listbox.itemconfig(tk.END, {'bg': '#e6be3b'})  # Жовтий для середнього
                    elif task["priority"] == "Низький":
                        self.task_listbox.insert(tk.END, task["title"])
                        self.task_listbox.itemconfig(tk.END, {'bg': 'green'})  # Зелений для низького


    def on_task_select(self, event):
        selection = event.widget.curselection()
        if selection:
            task_index = selection[0]
            task_name = event.widget.get(task_index)
            self.selected_task_name = task_name
            self.display_task_details(task_name)

    def display_task_details(self, task_name):
        task_file = f"./tasks/{task_name}.json"
        if os.path.exists(task_file):
            with open(task_file, "r", encoding="utf-8") as file:
                task = json.load(file)
                self.task_title_value.config(text=task["title"])
                self.task_description_value.config(text=task["description"])
                self.task_priority_value.config(text=task["priority"])
                self.task_status_value.config(text=task["status"])

    def add_task(self):
        task_data = self.task_input_dialog("Додати завдання")
        if task_data:
            task_file = f"./tasks/{task_data['title']}.json"
            with open(task_file, "w", encoding="utf-8") as file:
                json.dump(task_data, file, ensure_ascii=False, indent=4)
            self.load_tasks()
        else:
            task_data = None
            return task_data

    def edit_task(self):
        if self.selected_task_name:
            old_task_file = f"./tasks/{self.selected_task_name}.json"
            if os.path.exists(old_task_file):
                with open(old_task_file, "r", encoding="utf-8") as file:
                    task_data = json.load(file)
                updated_data = self.task_input_dialog("Редагувати завдання", task_data)
                if updated_data:
                    new_task_file = f"./tasks/{updated_data['title']}.json"
                    if old_task_file != new_task_file:
                        os.rename(old_task_file, new_task_file)  # Перейменовуємо файл
                    with open(new_task_file, "w", encoding="utf-8") as file:
                        json.dump(updated_data, file, ensure_ascii=False, indent=4)
                    self.load_tasks()

    def delete_task(self):
        if self.selected_task_name:
            task_file = f"./tasks/{self.selected_task_name}.json"
            if os.path.exists(task_file):
                os.remove(task_file)
                self.load_tasks()

    def open_task(self):
        if self.selected_task_name:
            task_file = f"./tasks/{self.selected_task_name}.json"
            if os.path.exists(task_file):
                with open(task_file, "r", encoding="utf-8") as file:
                    task_data = json.load(file)
                    if "open" in task_data and task_data["open"]:
                        webbrowser.open(task_data["open"])

    def filter_tasks(self, filter_type):
        tasks = []
        for filename in os.listdir("./tasks"):
            if filename.endswith(".json"):
                with open(f"./tasks/{filename}", "r", encoding="utf-8") as file:
                    task = json.load(file)
                    tasks.append(task)
        if filter_type == "status":
            tasks.sort(key=lambda x: x["status"])
        elif filter_type == "priority":
            priority_order = {"Високий": 1, "Середній": 2, "Низький": 3}
            tasks.sort(key=lambda x: priority_order[x["priority"]])

        self.task_listbox.delete(0, tk.END)
        for task in tasks:
            if task["priority"] == "Високий":
                self.task_listbox.insert(tk.END, task["title"])
                self.task_listbox.itemconfig(tk.END, {'bg': 'red'})  # Червоний для високого пріоритету
            elif task["priority"] == "Середній":
                self.task_listbox.insert(tk.END, task["title"])
                self.task_listbox.itemconfig(tk.END, {'bg': '#e6be3b'})  # Жовтий для середнього
            elif task["priority"] == "Низький":
                self.task_listbox.insert(tk.END, task["title"])
                self.task_listbox.itemconfig(tk.END, {'bg': 'green'})

    def task_input_dialog(self, title, task_data=None):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("450x450")
        dialog.config(bg="#2e2e2e")

        title_label = tk.Label(dialog, text="Назва:", bg="#2e2e2e", fg="white")
        title_label.pack(pady=5)
        title_entry = tk.Entry(dialog)
        title_entry.pack(pady=5)
        if task_data:
            title_entry.insert(0, task_data["title"])

        description_label = tk.Label(dialog, text="Опис:", bg="#2e2e2e", fg="white")
        description_label.pack(pady=5)
        description_entry = tk.Entry(dialog)
        description_entry.pack(pady=5)
        if task_data:
            description_entry.insert(0, task_data["description"])

        priority_label = tk.Label(dialog, text="Пріоритет:", bg="#2e2e2e", fg="white")
        priority_label.pack(pady=5)
        priority_var = tk.StringVar(value="Середній")
        priority_menu = tk.OptionMenu(dialog, priority_var, "Високий", "Середній", "Низький")
        priority_menu.pack(pady=5)
        if task_data:
            priority_var.set(task_data["priority"])

        status_label = tk.Label(dialog, text="Статус:", bg="#2e2e2e", fg="white")
        status_label.pack(pady=5)
        status_var = tk.StringVar(value="Непочате")
        status_menu = tk.OptionMenu(dialog, status_var, "Непочате", "В процесі", "Виконано")
        status_menu.pack(pady=5)
        if task_data:
            status_var.set(task_data["status"])

        open_label = tk.Label(dialog, text="Open URL/Path (необов'язково):", bg="#2e2e2e", fg="white")
        open_label.pack(pady=5)
        open_entry = tk.Entry(dialog)
        open_entry.pack(pady=5)
        if task_data and "open" in task_data:
            open_entry.insert(0, task_data["open"])

        # Додати кнопку "browse"
        def browse_file():
            filename = filedialog.askopenfilename()
            if filename:
                open_entry.delete(0, tk.END)
                open_entry.insert(0, filename)

        browse_button = tk.Button(dialog, text="Browse File", command=browse_file, bg="#4a4a4a", fg="white")
        browse_button.pack(pady=5)
        
        def browse_folder():
            foldername = filedialog.askdirectory()
            if foldername:
                open_entry.delete(0, tk.END)
                open_entry.insert(0, foldername)

        browse_folder_button = tk.Button(dialog, text="Browse Folder", command=browse_folder, bg="#4a4a4a", fg="white")
        browse_folder_button.pack(pady=5)

        def submit():
            title = title_entry.get()
            description = description_entry.get()
            priority = priority_var.get()
            status = status_var.get()
            open_path = open_entry.get()

            if title == "" or description == "":
                messagebox.showerror("ValueError","VALUE")
                return
            else:
                task = {
                    "title": title,
                    "description": description,
                    "priority": priority,
                    "status": status,
                    "open": open_path
                }
                dialog.destroy()  # Закриваємо вікно після того, як всі дані зібрані
                return task

        submit_button = tk.Button(dialog, text="Зберегти", command=lambda: submit_and_close(), bg="#4a4a4a", fg="white")
        submit_button.pack(pady=20)

        # Окрема функція для збору і закриття діалогу
        def submit_and_close():
            task = submit()
            if task:  # Перевіряємо, чи повернулося завдання (якщо було заповнено всі поля)
                dialog.grab_release()  # Вивільнення захоплення перед закриттям діалогу
                self.task_data = task

        dialog.grab_set()
        self.root.wait_window(dialog)

        return self.task_data


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
