
from tkcalendar import DateEntry
import sqlite3
import customtkinter as custk
from tkinter import messagebox

# Book lesson
class BookLesson(custk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.label = custk.CTkLabel(self, text="Book a Lesson")
        self.label.grid(row=0, column=0, columnspan=4, sticky="nsew")

        self.lesson_widgets()

        # Configure column weights to make widgets stretch
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

    def lesson_widgets(self):
        lesson_types = ["Baking Lesson", "Barista Lesson", "Both"]
        times = ["8:00","9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]

        lesson_label = custk.CTkLabel(self, text="Lesson Type: ")
        self.lesson_combobox = custk.CTkComboBox(self, values=lesson_types, state="readonly")

        date_label = custk.CTkLabel(self, text="Date: ")
        self.date_entry = DateEntry(self, year=2023, month=11, day=30, state="readonly")

        time_label = custk.CTkLabel(self, text="Time: ")
        self.time_combobox = custk.CTkComboBox(self, values=times, state="readonly")

        fname_label = custk.CTkLabel(self, text="First Name: ")
        self.fname_entry = custk.CTkEntry(self)

        save_button = custk.CTkButton(self, text="Save", command=self.save_to_lesson_book_database, border_width= 3, border_color= "black")

        # Place widgets
        lesson_label.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.lesson_combobox.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        date_label.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        self.date_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        time_label.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
        self.time_combobox.grid(row=4, column=1, sticky="ew", padx=5, pady=5)

        fname_label.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        self.fname_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

        save_button.grid(row=5, column=0, columnspan=4, sticky="nsew", pady=10)

    def save_to_lesson_book_database(self):
        lesson_type = self.lesson_combobox.get()
        date = self.date_entry.get()
        time = self.time_combobox.get()
        fname = self.fname_entry.get()

        if not all([lesson_type, date, time, fname]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        if not fname.isalpha():
            messagebox.showerror("Error", "Please only use letters in field: First Name")
            return

        conn = sqlite3.connect("lesson_book.db")
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS lessons
                          (lesson_type TEXT, date TEXT, time TEXT, fname TEXT)''')

        cursor.execute("INSERT INTO lessons VALUES (?, ?, ?, ?)", (lesson_type, date, time, fname))

        conn.commit()
        conn.close()

        messagebox.showinfo("Book lesson", "Lesson booked!")