# timetable_app/gui.py

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from data_manager import *
from reminders import check_reminders

class TimetableApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Timetable App")
        self.geometry("800x600")
        initialize_files()

        # Notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        # Tabs
        self.add_tab = ttk.Frame(self.notebook)
        self.view_tab = ttk.Frame(self.notebook)
        self.edit_tab = ttk.Frame(self.notebook)
        self.delete_tab = ttk.Frame(self.notebook)
        self.conflicts_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.add_tab, text='Add Entry')
        self.notebook.add(self.view_tab, text='View Schedule')
        self.notebook.add(self.edit_tab, text='Edit Entry')
        self.notebook.add(self.delete_tab, text='Delete Entry')
        self.notebook.add(self.conflicts_tab, text='Check Conflicts')

        self.setup_add_tab()
        self.setup_view_tab()
        self.setup_edit_tab()
        self.setup_delete_tab()
        self.setup_conflicts_tab()

        # Start reminders in background
        threading.Thread(target=check_reminders, daemon=True).start()

    def setup_add_tab(self):
        tk.Label(self.add_tab, text="Entry Type:").grid(row=0, column=0, pady=5)
        self.entry_type = tk.StringVar()
        ttk.Combobox(self.add_tab, textvariable=self.entry_type, values=['Lesson', 'Exam', 'Routine']).grid(row=0, column=1)

        tk.Label(self.add_tab, text="Name:").grid(row=1, column=0, pady=5)
        self.name_entry = tk.Entry(self.add_tab)
        self.name_entry.grid(row=1, column=1)

        tk.Label(self.add_tab, text="Date (for Lesson/Exam, YYYY-MM-DD):").grid(row=2, column=0, pady=5)
        self.date_entry = tk.Entry(self.add_tab)
        self.date_entry.grid(row=2, column=1)

        tk.Label(self.add_tab, text="Start Time (HH:MM):").grid(row=3, column=0, pady=5)
        self.start_time_entry = tk.Entry(self.add_tab)
        self.start_time_entry.grid(row=3, column=1)

        tk.Label(self.add_tab, text="End Time (HH:MM):").grid(row=4, column=0, pady=5)
        self.end_time_entry = tk.Entry(self.add_tab)
        self.end_time_entry.grid(row=4, column=1)

        tk.Label(self.add_tab, text="Day of Week (for Routine, e.g., Monday or Everyday):").grid(row=5, column=0, pady=5)
        self.day_week_entry = tk.Entry(self.add_tab)
        self.day_week_entry.grid(row=5, column=1)

        tk.Label(self.add_tab, text="Location (for Lesson/Exam):").grid(row=6, column=0, pady=5)
        self.location_entry = tk.Entry(self.add_tab)
        self.location_entry.grid(row=6, column=1)

        tk.Label(self.add_tab, text="Notes:").grid(row=7, column=0, pady=5)
        self.notes_entry = tk.Entry(self.add_tab)
        self.notes_entry.grid(row=7, column=1)

        ttk.Button(self.add_tab, text="Add", command=self.add_entry).grid(row=8, column=1, pady=10)

    def add_entry(self):
        entry_type = self.entry_type.get().lower()
        name = self.name_entry.get().strip()
        start_time = self.start_time_entry.get().strip()
        end_time = self.end_time_entry.get().strip()
        notes = self.notes_entry.get().strip()

        if not name:
            messagebox.showerror("Error", "Name is required.")
            return

        if not (start_time and end_time):
            messagebox.showerror("Error", "Start and End times are required.")
            return

        try:
            if entry_type in ['lesson', 'exam']:
                date = self.date_entry.get().strip()
                location = self.location_entry.get().strip()
                if not date:
                    raise ValueError("Date is required for Lesson/Exam.")
                add_lesson_exam(entry_type, name, date, start_time, end_time, location, notes)
            elif entry_type == 'routine':
                day_of_week = self.day_week_entry.get().strip()
                if not day_of_week:
                    raise ValueError("Day of Week is required for Routine.")
                add_routine(name, start_time, end_time, day_of_week, notes)
            else:
                raise ValueError("Invalid entry type selected.")

            messagebox.showinfo("Success", "Entry added!")
            # Clear fields after success
            self.name_entry.delete(0, tk.END)
            self.start_time_entry.delete(0, tk.END)
            self.end_time_entry.delete(0, tk.END)
            self.day_week_entry.delete(0, tk.END)
            self.location_entry.delete(0, tk.END)
            self.notes_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def setup_view_tab(self):
        tk.Label(self.view_tab, text="View Type:").grid(row=0, column=0, pady=5)
        self.view_type = tk.StringVar()
        ttk.Combobox(self.view_tab, textvariable=self.view_type, values=['Daily', 'Weekly', 'Semester', 'Upcoming']).grid(row=0, column=1)

        tk.Label(self.view_tab, text="Date/Start Date (YYYY-MM-DD):").grid(row=1, column=0, pady=5)
        self.view_date = tk.Entry(self.view_tab)
        self.view_date.grid(row=1, column=1)

        ttk.Button(self.view_tab, text="View", command=self.view_schedule).grid(row=2, column=1, pady=10)

        self.view_text = tk.Text(self.view_tab, height=20, width=80)
        self.view_text.grid(row=3, column=0, columnspan=2)

    def view_schedule(self):
        self.view_text.delete(1.0, tk.END)
        view_type = self.view_type.get().lower()
        date = self.view_date.get().strip()

        if view_type in ['daily', 'weekly'] and not date:
            messagebox.showerror("Error", "Date is required for this view.")
            return

        try:
            if view_type == 'daily':
                lessons, routines = get_daily_schedule(date)
                self.view_text.insert(tk.END, "Lessons/Exams:\n" + lessons.to_string() + "\n\nRoutines:\n" + routines.to_string())
            elif view_type == 'weekly':
                weekly = get_weekly_schedule(date)
                for day, (lessons, routines) in weekly.items():
                    self.view_text.insert(tk.END, f"{day}:\nLessons/Exams:\n{lessons.to_string() if not lessons.empty else 'None'}\nRoutines:\n{routines.to_string() if not routines.empty else 'None'}\n\n")
            elif view_type == 'semester':
                lessons, routines = get_semester_schedule()
                self.view_text.insert(tk.END, "All Lessons/Exams:\n" + lessons.to_string() + "\n\nAll Routines:\n" + routines.to_string())
            elif view_type == 'upcoming':
                upcoming = get_upcoming_events()
                self.view_text.insert(tk.END, "Upcoming Events:\n" + upcoming.to_string())
        except ValueError as ve:
            messagebox.showerror("Error", f"Invalid date format: {str(ve)}")

    def setup_edit_tab(self):
        tk.Label(self.edit_tab, text="Entry Type:").grid(row=0, column=0, pady=5)
        self.edit_type = tk.StringVar()
        ttk.Combobox(self.edit_tab, textvariable=self.edit_type, values=['Lesson/Exam', 'Routine']).grid(row=0, column=1)

        ttk.Button(self.edit_tab, text="Load Entries", command=self.load_for_edit).grid(row=1, column=1, pady=5)

        self.edit_tree = ttk.Treeview(self.edit_tab, columns=('Index', 'Name', 'Date/Day', 'Start', 'End'), show='headings')
        self.edit_tree.heading('Index', text='Index')
        self.edit_tree.heading('Name', text='Name')
        self.edit_tree.heading('Date/Day', text='Date/Day')
        self.edit_tree.heading('Start', text='Start')
        self.edit_tree.heading('End', text='End')
        self.edit_tree.grid(row=2, column=0, columnspan=2)

        # Form for editing
        tk.Label(self.edit_tab, text="Selected Index:").grid(row=3, column=0, pady=5)
        self.edit_index = tk.Entry(self.edit_tab)
        self.edit_index.grid(row=3, column=1)

        tk.Label(self.edit_tab, text="New Name:").grid(row=4, column=0, pady=5)
        self.edit_name = tk.Entry(self.edit_tab)
        self.edit_name.grid(row=4, column=1)

        tk.Label(self.edit_tab, text="New Date/Day (YYYY-MM-DD for Date):").grid(row=5, column=0, pady=5)
        self.edit_date_day = tk.Entry(self.edit_tab)
        self.edit_date_day.grid(row=5, column=1)

        tk.Label(self.edit_tab, text="New Start Time:").grid(row=6, column=0, pady=5)
        self.edit_start = tk.Entry(self.edit_tab)
        self.edit_start.grid(row=6, column=1)

        tk.Label(self.edit_tab, text="New End Time:").grid(row=7, column=0, pady=5)
        self.edit_end = tk.Entry(self.edit_tab)
        self.edit_end.grid(row=7, column=1)

        tk.Label(self.edit_tab, text="New Location/Notes:").grid(row=8, column=0, pady=5)
        self.edit_extra = tk.Entry(self.edit_tab)
        self.edit_extra.grid(row=8, column=1)

        ttk.Button(self.edit_tab, text="Update", command=self.update_entry).grid(row=9, column=1, pady=10)

    def load_for_edit(self):
        self.edit_tree.delete(*self.edit_tree.get_children())
        entry_type = self.edit_type.get().lower()
        if entry_type == 'lesson/exam':
            df = load_lessons()
            for idx, row in df.iterrows():
                self.edit_tree.insert('', 'end', values=(idx, row['Name'], row['Date'], row['Start_Time'], row['End_Time']))
        elif entry_type == 'routine':
            df = load_routines()
            for idx, row in df.iterrows():
                self.edit_tree.insert('', 'end', values=(idx, row['Name'], row['Day_of_Week'], row['Start_Time'], row['End_Time']))

    def update_entry(self):
        entry_type = self.edit_type.get().lower()
        try:
            index = int(self.edit_index.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid index")
            return

        updates = {}
        if self.edit_name.get():
            updates['Name'] = self.edit_name.get()
        if self.edit_date_day.get():
            if entry_type == 'lesson/exam':
                updates['Date'] = self.edit_date_day.get()
            else:
                updates['Day_of_Week'] = self.edit_date_day.get()
        if self.edit_start.get():
            updates['Start_Time'] = self.edit_start.get()
        if self.edit_end.get():
            updates['End_Time'] = self.edit_end.get()
        if self.edit_extra.get():
            if entry_type == 'lesson/exam':
                updates['Location'] = self.edit_extra.get()
            else:
                updates['Notes'] = self.edit_extra.get()

        try:
            if entry_type == 'lesson/exam':
                edit_lesson_exam(index, updates)
            else:
                edit_routine(index, updates)
            messagebox.showinfo("Success", "Entry updated!")
            self.load_for_edit()
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def setup_delete_tab(self):
        tk.Label(self.delete_tab, text="Entry Type:").grid(row=0, column=0, pady=5)
        self.delete_type = tk.StringVar()
        ttk.Combobox(self.delete_tab, textvariable=self.delete_type, values=['Lesson/Exam', 'Routine']).grid(row=0, column=1)

        ttk.Button(self.delete_tab, text="Load Entries", command=self.load_for_delete).grid(row=1, column=1, pady=5)

        self.delete_tree = ttk.Treeview(self.delete_tab, columns=('Index', 'Name', 'Date/Day', 'Start', 'End'), show='headings')
        self.delete_tree.heading('Index', text='Index')
        self.delete_tree.heading('Name', text='Name')
        self.delete_tree.heading('Date/Day', text='Date/Day')
        self.delete_tree.heading('Start', text='Start')
        self.delete_tree.heading('End', text='End')
        self.delete_tree.grid(row=2, column=0, columnspan=2)

        tk.Label(self.delete_tab, text="Index to Delete:").grid(row=3, column=0, pady=5)
        self.delete_index = tk.Entry(self.delete_tab)
        self.delete_index.grid(row=3, column=1)

        ttk.Button(self.delete_tab, text="Delete", command=self.delete_entry).grid(row=4, column=1, pady=10)

    def load_for_delete(self):
        self.delete_tree.delete(*self.delete_tree.get_children())
        entry_type = self.delete_type.get().lower()
        if entry_type == 'lesson/exam':
            df = load_lessons()
            for idx, row in df.iterrows():
                self.delete_tree.insert('', 'end', values=(idx, row['Name'], row['Date'], row['Start_Time'], row['End_Time']))
        elif entry_type == 'routine':
            df = load_routines()
            for idx, row in df.iterrows():
                self.delete_tree.insert('', 'end', values=(idx, row['Name'], row['Day_of_Week'], row['Start_Time'], row['End_Time']))

    def delete_entry(self):
        entry_type = self.delete_type.get().lower()
        try:
            index = int(self.delete_index.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid index")
            return

        if entry_type == 'lesson/exam':
            delete_lesson_exam(index)
        else:
            delete_routine(index)
        messagebox.showinfo("Success", "Entry deleted!")
        self.load_for_delete()

    def setup_conflicts_tab(self):
        tk.Label(self.conflicts_tab, text="Date to Check (YYYY-MM-DD):").grid(row=0, column=0, pady=5)
        self.conflicts_date = tk.Entry(self.conflicts_tab)
        self.conflicts_date.grid(row=0, column=1)

        ttk.Button(self.conflicts_tab, text="Check", command=self.show_conflicts).grid(row=1, column=1, pady=10)

        self.conflicts_text = tk.Text(self.conflicts_tab, height=20, width=80)
        self.conflicts_text.grid(row=2, column=0, columnspan=2)

    def show_conflicts(self):
        self.conflicts_text.delete(1.0, tk.END)
        date = self.conflicts_date.get().strip()
        if not date:
            messagebox.showerror("Error", "Date is required.")
            return
        try:
            conflicts = check_conflicts(date)
            if not conflicts:
                self.conflicts_text.insert(tk.END, "No conflicts.")
            else:
                for c in conflicts:
                    self.conflicts_text.insert(tk.END, c + "\n")
        except ValueError as ve:
            messagebox.showerror("Error", f"Invalid date format: {str(ve)}")