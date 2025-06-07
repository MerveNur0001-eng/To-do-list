import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import pygame
import threading
import time
import json
import os

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.root.geometry("600x750")


        self.theme_colors = {
            "Purple Mode": {
                "bg": "#7A316F", "fg": "white", "active_bg": "blue", "button_fg": "white", "button_active_bg": "#E966A0"
            },
            "Blue Mode": {
                "bg": "#1F4172", "fg": "white", "active_bg": "#142D5C", "button_fg": "white", "button_active_bg": "#3ABEF9"
            },
            "Green Mode": {
                "bg": "dark green", "fg": "white", "active_bg": "#27AE60", "button_fg": "white", "button_active_bg": "light green"
            },
            "Orange Mode": {
                "bg": "orange", "fg": "black", "active_bg": "#F39C12", "button_fg": "black", "button_active_bg": "#E67E22"
            }
        }
        self.current_theme = tk.StringVar(value="Purple Mode")

        self.tasks = []
        self.current_category = tk.StringVar()
        self.current_category.set("All")
        self.current_importance = tk.StringVar()
        self.current_importance.set("Low")

        self.completed_tasks_file = "completed_tasks.json"
        self.load_completed_tasks()

        self.create_widgets()
        self.update_theme()

        pygame.mixer.init()

        self.reminder_thread = None
        self.reminder_time = 0
    def create_widgets(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.theme_button_canvas = tk.Canvas(self.root, width=50, height=50, highlightthickness=0, bg="#937DC2")
        self.theme_button_canvas.place(x=10, y=10)
        self.round_image = tk.PhotoImage(file="Image-sound/palette.png").subsample(9, 9)
        self.theme_button_canvas.create_image(25, 25, image=self.round_image)
        self.theme_button_canvas.bind("<Button-1>", self.open_theme_menu)

        self.completed_tasks_button = tk.Button(self.root, text=f"Deleted Tasks ({len(self.completed_tasks)})", command=self.show_completed_tasks)
        self.completed_tasks_button.place(x=490, y=10)

        self.add_image_button("Image-sound/ddelete.png", self.delete_selected, 275, 690)

        self.category_label = ttk.Label(self.root, text="Category:", font=("Arial", 12, "bold"))
        self.category_label.pack(pady=5)
        self.category_combobox = ttk.Combobox(self.root, textvariable=self.current_category,
                                              values=["All", "General", "Work", "Personal", "School", "Shopping"],
                                              state="readonly", font=("Arial", 10))
        self.category_combobox.pack(pady=5)


        self.importance_label = ttk.Label(self.root, text="Importance:", font=("Arial", 12, "bold"))
        self.importance_label.pack(pady=5)
        self.importance_combobox = ttk.Combobox(self.root, textvariable=self.current_importance,
                                                values=["Low", "Medium", "High"], state="readonly",
                                                font=("Arial", 10))
        self.importance_combobox.pack(pady=5)

        # Görev giriş alanı
        self.task_entry = ttk.Entry(self.root, width=40, font=("Arial", 10))
        self.task_entry.pack(pady=5)

        self.deadline_label = ttk.Label(self.root, text="Deadline:                Reminder:", font=("Arial", 12, "bold"))
        self.deadline_label.pack(pady=5)
        self.deadline_frame = tk.Frame(self.root)
        self.deadline_frame.pack(pady=5)

        self.date_label = ttk.Label(self.deadline_frame, text="Date:", font=("Arial", 10))
        self.date_label.pack(side=tk.LEFT)
        self.deadline_calendar = DateEntry(self.deadline_frame, width=12, background="white", foreground="black",
                                           borderwidth=2, font=("Arial", 10))
        self.deadline_calendar.pack(side=tk.LEFT)

        self.hour_label = ttk.Label(self.deadline_frame, text="Hour:", font=("Arial", 10))
        self.hour_label.pack(side=tk.LEFT)
        self.hour_combobox = ttk.Combobox(self.deadline_frame, values=[str(i).zfill(2) for i in range(24)],
                                          state="readonly", font=("Arial", 10), width=3)
        self.hour_combobox.pack(side=tk.LEFT)
        self.minute_label = ttk.Label(self.deadline_frame, text="Minute:", font=("Arial", 10))
        self.minute_label.pack(side=tk.LEFT)
        self.minute_combobox = ttk.Combobox(self.deadline_frame, values=[str(i).zfill(2) for i in range(60)],
                                            state="readonly", font=("Arial", 10), width=3)
        self.minute_combobox.pack(side=tk.LEFT)


        self.add_button = ttk.Button(self.root, text="Add Task", command=self.add_task, style="Add.TButton")
        self.add_button.pack(pady=5)

        self.edit_button = ttk.Button(self.root, text="Edit Task", command=self.edit_task, style="Edit.TButton")
        self.edit_button.pack(pady=5)

        self.sort_button = ttk.Button(self.root, text="Sort", style="Sort.TButton")
        self.sort_button.pack(pady=5)
        self.sort_button.bind("<Button-1>", self.show_sort_menu)

        self.task_treeview = ttk.Treeview(self.root, columns=("Task", "Category", "Deadline", "Importance", "Completed"),
                                          show="headings", selectmode="extended")
        self.task_treeview.heading("Task", text="Task", anchor="center")
        self.task_treeview.heading("Category", text="Category", anchor="center")
        self.task_treeview.heading("Deadline", text="Deadline", anchor="center")
        self.task_treeview.heading("Importance", text="Importance", anchor="center")
        self.task_treeview.heading("Completed", text="Completed", anchor="center")
        self.task_treeview.pack(pady=10)

        self.task_treeview.column("Task", width=125)
        self.task_treeview.column("Category", width=125)
        self.task_treeview.column("Deadline", width=125)
        self.task_treeview.column("Importance", width=125)
        self.task_treeview.column("Completed", width=100)

        self.task_treeview.bind("<Button-1>", self.populate_entry_fields)
        self.task_treeview.bind("<Double-1>", self.populate_entry_fields)

        self.configure_importance_tags(self.task_treeview)

        self.complete_button = ttk.Button(self.root, text="Complete Tasks", command=self.complete_selected, style="Complete.TButton")
        self.complete_button.pack(pady=5)

        self.uncomplete_button = ttk.Button(self.root, text="Uncomplete Tasks", command=self.uncomplete_selected, style="Uncomplete.TButton")
        self.uncomplete_button.pack(pady=5)

        self.update_task_treeview()

    def add_image_button(self, image_path, command, x, y):
        image = Image.open(image_path)
        resized_image = image.resize((30, 30))
        photo = ImageTk.PhotoImage(resized_image)
        button = ttk.Button(self.root, image=photo, command=command, style="Toolbutton.TButton")
        button.image = photo
        button.place(x=x, y=y)

    def open_theme_menu(self, event):
        self.theme_menu = tk.Menu(self.root, tearoff=False)
        for theme in self.theme_colors.keys():
            self.theme_menu.add_radiobutton(label=theme, variable=self.current_theme, value=theme,
                                            command=self.update_theme)
        self.theme_menu.post(self.theme_button_canvas.winfo_rootx(),
                             self.theme_button_canvas.winfo_rooty() + self.theme_button_canvas.winfo_height())

    def add_task(self):
        task = self.task_entry.get().strip()
        deadline_date = self.deadline_calendar.get_date()
        hour = self.hour_combobox.get()
        minute = self.minute_combobox.get()
        category = self.current_category.get()
        importance = self.current_importance.get()

        if task:
            try:
                deadline = deadline_date.strftime('%Y-%m-%d') + f" {hour}:{minute}"
                self.tasks.append({"task": task, "deadline": deadline, "category": category, "importance": importance, "completed": False})
                self.update_task_treeview()
                self.task_entry.delete(0, tk.END)
                self.schedule_reminder()
            except ValueError:
                messagebox.showerror("Error", "Invalid deadline format.")
        else:
            messagebox.showerror("Error", "Please enter the task.")

    def edit_task(self):
        selected_items = self.task_treeview.selection()
        if len(selected_items) != 1:
            messagebox.showerror("Error", "Please select a single task to edit.")
            return

        selected_item = selected_items[0]
        index = self.task_treeview.index(selected_item)
        edited_task = self.task_entry.get().strip()
        edited_deadline_date = self.deadline_calendar.get_date()
        edited_hour = self.hour_combobox.get()
        edited_minute = self.minute_combobox.get()
        edited_category = self.current_category.get()
        edited_importance = self.current_importance.get()

        if edited_task:
            try:
                edited_deadline = edited_deadline_date.strftime('%Y-%m-%d') + f" {edited_hour}:{edited_minute}"
                self.tasks[index]["task"] = edited_task
                self.tasks[index]["deadline"] = edited_deadline
                self.tasks[index]["category"] = edited_category
                self.tasks[index]["importance"] = edited_importance
                self.update_task_treeview()
                self.task_entry.delete(0, tk.END)
                self.task_treeview.selection_remove(selected_item)
                self.schedule_reminder()
            except ValueError:
                messagebox.showerror("Error", "Invalid deadline format.")
        else:
            messagebox.showerror("Error", "Please enter the task.")

    def complete_selected(self):
        selected_items = self.task_treeview.selection()
        for item in selected_items:
            index = self.task_treeview.index(item)
            self.tasks[index]["completed"] = True
            self.play_checkmark_sound()
        self.update_task_treeview()

    def uncomplete_selected(self):
        selected_items = self.task_treeview.selection()
        for item in selected_items:
            index = self.task_treeview.index(item)
            self.tasks[index]["completed"] = False
        self.update_task_treeview()

    def delete_selected(self):
        selected_items = self.task_treeview.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "No tasks selected to delete.")
            return

        selected_indices = [self.task_treeview.index(item) for item in selected_items]
        selected_indices.sort(reverse=True)

        for index in selected_indices:
            self.save_completed_task(self.tasks[index])
            del self.tasks[index]

        self.update_task_treeview()
        self.update_completed_tasks_window()

    def update_completed_tasks_window(self):
        if hasattr(self, "completed_tasks_window") and self.completed_tasks_window.winfo_exists():
            self.load_completed_tasks()
            self.completed_tasks_treeview.delete(*self.completed_tasks_treeview.get_children())

            for task in self.completed_tasks:
                importance_color = self.get_importance_color(task["importance"])
                self.completed_tasks_treeview.insert("", "end",
                                                     values=(
                                                         task["task"],
                                                         task["category"],
                                                         task["deadline"],
                                                         task["importance"]
                                                     ), tags=(importance_color,))

    def update_task_treeview(self):
        self.task_treeview.delete(*self.task_treeview.get_children())

        for task in self.tasks:
            completed_status = "✔ " if task["completed"] else ""
            importance_color = self.get_importance_color(task["importance"])
            self.task_treeview.insert("", "end",
                                      values=(
                                          f"{completed_status}{task['task']}",
                                          task["category"],
                                          task["deadline"],
                                          task["importance"],
                                          "Completed" if task["completed"] else "Not Completed"
                                      ), tags=(importance_color,))

        self.completed_tasks_button.config(text=f"Deleted Tasks ({len(self.completed_tasks)})")

    def get_importance_color(self, importance):
        if importance == "Low":
            return "low_importance"
        elif importance == "Medium":
            return "medium_importance"
        elif importance == "High":
            return "high_importance"
        return ""

    def update_theme(self):
        theme_name = self.current_theme.get()
        theme = self.theme_colors[theme_name]
        background_color = theme["bg"]
        foreground_color = theme["fg"]
        active_bg_color = theme["active_bg"]
        button_fg_color = theme["button_fg"]
        button_active_bg_color = theme["button_active_bg"]

        self.root.configure(bg=background_color)
        self.category_label.configure(background=background_color, foreground=foreground_color)
        self.importance_label.configure(background=background_color, foreground=foreground_color)
        self.deadline_label.configure(background=background_color, foreground=foreground_color)
        self.date_label.configure(background=background_color, foreground=foreground_color)
        self.hour_label.configure(background=background_color, foreground=foreground_color)
        self.minute_label.configure(background=background_color, foreground=foreground_color)

        self.style.configure("TLabel", background=background_color, foreground=foreground_color)
        self.style.configure("TButton", background=background_color, foreground=foreground_color)
        self.style.configure("Add.TButton", font=("Arial", 10, "bold"), background=background_color, foreground=button_fg_color)
        self.style.map("Add.TButton", background=[("active", button_active_bg_color)])
        self.style.configure("Edit.TButton", font=("Arial", 10, "bold"), background=background_color, foreground=button_fg_color)
        self.style.map("Edit.TButton", background=[("active", button_active_bg_color)])
        self.style.configure("Sort.TButton", font=("Arial", 10, "bold"), background=background_color, foreground=button_fg_color)
        self.style.map("Sort.TButton", background=[("active", button_active_bg_color)])
        self.style.configure("Complete.TButton", font=("Arial", 10, "bold"), background=background_color, foreground=button_fg_color)
        self.style.map("Complete.TButton", background=[("active", button_active_bg_color)])
        self.style.configure("Uncomplete.TButton", font=("Arial", 10, "bold"), background=background_color, foreground=button_fg_color)
        self.style.map("Uncomplete.TButton", background=[("active", button_active_bg_color)])
        self.style.configure("Toolbutton.TButton", background=background_color, foreground=button_fg_color)
        self.style.map("Toolbutton.TButton", background=[("active", button_active_bg_color)])

        self.theme_button_canvas.configure(bg=background_color)

    def show_completed_tasks(self):
        self.load_completed_tasks()
        self.completed_tasks_window = tk.Toplevel(self.root)
        self.completed_tasks_window.title("Deleted Tasks")
        self.completed_tasks_window.geometry("600x680")

        self.completed_tasks_window.configure(bg="#ADB2D4")

        frame = ttk.Frame(self.completed_tasks_window)
        frame.pack(fill=tk.BOTH, expand=True)

        self.completed_tasks_treeview = ttk.Treeview(frame, columns=("Task", "Category", "Deadline", "Importance"),
                                                     show="headings")
        self.completed_tasks_treeview.heading("Task", text="Task", anchor="center")
        self.completed_tasks_treeview.heading("Category", text="Category", anchor="center")
        self.completed_tasks_treeview.heading("Deadline", text="Deadline", anchor="center")
        self.completed_tasks_treeview.heading("Importance", text="Importance", anchor="center")

        self.completed_tasks_treeview.column("Task", width=150)
        self.completed_tasks_treeview.column("Category", width=150)
        self.completed_tasks_treeview.column("Deadline", width=150)
        self.completed_tasks_treeview.column("Importance", width=150)

        self.completed_tasks_treeview.pack(fill=tk.BOTH, expand=True)

        scrollbar_y = ttk.Scrollbar(frame, orient="vertical", command=self.completed_tasks_treeview.yview)
        self.completed_tasks_treeview.configure(yscroll=scrollbar_y.set)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        scrollbar_x = ttk.Scrollbar(frame, orient="horizontal", command=self.completed_tasks_treeview.xview)
        self.completed_tasks_treeview.configure(xscroll=scrollbar_x.set)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.configure_importance_tags(self.completed_tasks_treeview)

        for task in self.completed_tasks:
            importance_color = self.get_importance_color(task["importance"])
            self.completed_tasks_treeview.insert("", "end",
                                                 values=(
                                                     task["task"],
                                                     task["category"],
                                                     task["deadline"],
                                                     task["importance"]
                                                 ), tags=(importance_color,))

        button_frame = ttk.Frame(self.completed_tasks_window)
        button_frame.pack(fill=tk.X, pady=5)

        delete_button = ttk.Button(button_frame, text="Delete Selected",
                                   command=lambda: self.delete_selected_completed(self.completed_tasks_treeview))
        delete_button.pack(side=tk.LEFT, padx=5)

        back_button = ttk.Button(button_frame, text="Back", command=self.completed_tasks_window.destroy)
        back_button.pack(side=tk.RIGHT, padx=5)

    def save_completed_task(self, task):
        self.completed_tasks.append(task)
        with open(self.completed_tasks_file, 'w') as file:
            json.dump(self.completed_tasks, file, indent=4)

    def load_completed_tasks(self):
        try:
            with open(self.completed_tasks_file, 'r') as file:
                self.completed_tasks = json.load(file)
        except FileNotFoundError:
            self.completed_tasks = []

    def delete_selected_completed(self, treeview):
        selected_items = treeview.selection()
        selected_indices = [treeview.index(item) for item in selected_items]
        selected_indices.sort(reverse=True)
        for index in selected_indices:
            del self.completed_tasks[index]
        with open(self.completed_tasks_file, 'w') as file:
            json.dump(self.completed_tasks, file, indent=4)
        treeview.delete(*selected_items)
        self.completed_tasks_button.config(text=f"Deleted Tasks ({len(self.completed_tasks)})")
    def play_checkmark_sound(self):
        pygame.mixer.music.load("Image-sound/checkmark.mp3")
        pygame.mixer.music.play()

    def schedule_reminder(self):
        # Get the reminder time from the user or a predefined method
        reminder_time = self.get_reminder_time()

        # Check if the reminder time is valid (greater than 0)
        if reminder_time > 0:
            # Store the reminder time in the instance variable
            self.reminder_time = reminder_time

            # Schedule the reminder using the `after` method of Tkinter
            # Convert seconds to milliseconds (multiply by 1000)
            self.root.after(int(self.reminder_time * 1000), self.reminder)
        else:
            # Print an error message if the reminder time is invalid or in the past
            print("Reminder time is either expired or invalid.")

    def reminder(self):
        try:
            # Reinitialize the Pygame mixer
            pygame.mixer.init()

            # Get the absolute path to the reminder sound file
            reminder_sound_path = os.path.abspath("Image-sound/reminder_sound.mp3")

            # Check if the file exists
            if not os.path.exists(reminder_sound_path):
                raise FileNotFoundError(f"File not found: {reminder_sound_path}")

            # Load and play the reminder sound
            pygame.mixer.music.load(reminder_sound_path)
            pygame.mixer.music.play()

            # Show a pop-up reminder message
            messagebox.showinfo("Reminder", "You have a task, don't forget!")

        except FileNotFoundError as e:
            messagebox.showerror("Error", str(e))

        except pygame.error as e:
            messagebox.showerror("Error", f"Sound could not be played: {e}")

        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def get_reminder_time(self):
        from datetime import datetime
        try:
            deadline_date = self.deadline_calendar.get_date()
            reminder_hour = self.hour_combobox.get()
            reminder_minute = self.minute_combobox.get()
            deadline_str = f"{deadline_date} {reminder_hour}:{reminder_minute}"
            deadline_time = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
            current_time = datetime.now()
            time_difference = (deadline_time - current_time).total_seconds()
            return max(time_difference, 0)
        except ValueError:
            return 0


    def populate_entry_fields(self, event):
        selected_items = self.task_treeview.selection()
        if selected_items:
            index = self.task_treeview.index(selected_items[0])
            task = self.tasks[index]
            self.task_entry.delete(0, tk.END)
            self.task_entry.insert(0, task["task"])
            deadline_parts = task["deadline"].split(" ")
            deadline_date = deadline_parts[0]
            deadline_time = deadline_parts[1]
            deadline_year, deadline_month, deadline_day = map(int, deadline_date.split("-"))
            self.deadline_calendar.set_date(deadline_year, deadline_month, deadline_day)
            self.hour_combobox.set(deadline_time.split(":")[0])
            self.minute_combobox.set(deadline_time.split(":")[1])
            self.current_category.set(task["category"])
            self.current_importance.set(task["importance"])

    def show_sort_menu(self, event):
        self.sort_menu = tk.Menu(self.root, tearoff=False)
        self.sort_menu.add_command(label="Sort by Category", command=lambda: self.sort_tasks("category"))
        self.sort_menu.add_command(label="Sort by Deadline", command=lambda: self.sort_tasks("deadline"))
        self.sort_menu.add_command(label="Sort by Importance", command=lambda: self.sort_tasks("importance"))
        self.sort_menu.add_command(label="Sort by Completion", command=lambda: self.sort_tasks("completed"))
        self.sort_menu.post(self.sort_button.winfo_rootx(),
                            self.sort_button.winfo_rooty() + self.sort_button.winfo_height())

    def sort_tasks(self, criteria):
        if criteria == "completed":
            self.tasks.sort(key=lambda x: x[criteria], reverse=True)
        elif criteria == "importance":
            importance_order = {"Low": 2, "Medium": 1, "High": 0}
            self.tasks.sort(key=lambda x: importance_order.get(x[criteria]), reverse=False)
        else:
            self.tasks.sort(key=lambda x: x[criteria])
        self.update_task_treeview()

    def configure_importance_tags(self, treeview):
        treeview.tag_configure("low_importance", background="light green")
        treeview.tag_configure("medium_importance", background="orange")
        treeview.tag_configure("high_importance", background="#B82132")

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()