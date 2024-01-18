import tkinter as tk
import customtkinter as custk
from tkcalendar import DateEntry
import sqlite3
from tkinter import messagebox

#Book table
class BookTable(custk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.label = custk.CTkLabel(self, text="Book a Table")
        self.label.grid(row=0, column=0, columnspan=4, sticky="nsew")

        self.booking_widgets()

        # Configure column weights to make widgets stretch
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

    def booking_widgets(self):
        locations = ["Harrogate", "Leeds", "Knaresbourough Castle"]
        times = ["8:00","9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]
        
        def sliding(value):
            diner_slider_label.configure(text=int(value))

        location_label = custk.CTkLabel(self, text="Location: ")
        self.location_combobox = custk.CTkComboBox(self, values=locations, state="readonly")
        
        date_label = custk.CTkLabel(self, text="Date: ")
        self.date_entry = DateEntry(self, year=2023, month=11, day=30, state="readonly")

        time_label = custk.CTkLabel(self, text="Time: ")
        self.time_combobox = custk.CTkComboBox(self, values=times, state="readonly")

        seats_label = custk.CTkLabel(self, text="No. of Diners: ")
        self.seats_slider = custk.CTkSlider(self, from_=1, to=10, command=sliding)
        self.seats_slider.set(1)
        diner_slider_label = custk.CTkLabel(self, text="")

        fname_label = custk.CTkLabel(self, text="First Name: ")
        self.fname_entry = custk.CTkEntry(self)

        save_button = custk.CTkButton(self, text="Save", command=self.save_to_table_booking_database, border_width= 3, border_color= "black")

        # Place widgets
        location_label.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.location_combobox.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        date_label.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        self.date_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        time_label.grid(row=5, column=0, sticky="ew", padx=5, pady=5)
        self.time_combobox.grid(row=5, column=1, sticky="ew", padx=5, pady=5)

        seats_label.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        self.seats_slider.grid(row=3, column=1, sticky="ew", padx=5, pady=(5, 0))
        diner_slider_label.grid(row=4, column=1, sticky="nsew", padx=5, pady=(0, 5))

        fname_label.grid(row=5, column=0, sticky="ew", padx=5, pady=5)
        self.fname_entry.grid(row=5, column=1, sticky="ew", padx=5, pady=5)

        save_button.grid(row=6, column=0, columnspan=4, sticky="nsew", pady=10)

    def save_to_table_booking_database(self):
        location = self.location_combobox.get()
        date = self.date_entry.get()
        time = self.time_combobox.get()
        seats = self.seats_slider.get()
        fname = self.fname_entry.get()

        if not all([location, date, time, seats, fname]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        if not fname.isalpha():
            messagebox.showerror("Error", "Please only use letters in field: First Name")
            return

        conn = sqlite3.connect("table_booking.db")
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS tables
                          (location TEXT, date TEXT, time TEXT, seats INTEGER, fname TEXT)''')

        cursor.execute("INSERT INTO tables VALUES (?, ?, ?, ?, ?)", (location, date, time, seats, fname))

        conn.commit()
        conn.close()

        messagebox.showinfo("Book Table","Table Booked!")