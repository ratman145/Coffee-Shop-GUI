import customtkinter as custk
from tkcalendar import DateEntry
import sqlite3
from tkinter import messagebox

# Order Cake
class OrderCake(custk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.label = custk.CTkLabel(self, text="Order Cake")
        self.label.grid(row=0, column=0, columnspan=4, sticky="nsew")

        self.cake_widgets()

        # Configure column weights to make widgets stretch
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

    def cake_widgets(self):
        cake_types = ["Chocolate Cake", "Sponge Cake", "Rocky Road", "Carrot Cake", "Fruit Cake"]
        times = ["9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]

        def sliding(value):
            cake_slider_label.configure(text=int(value))

        cake_label = custk.CTkLabel(self, text="Cake Type: ")
        self.cake_combobox = custk.CTkComboBox(self, values=cake_types)

        date_label = custk.CTkLabel(self, text="Pick-up Date: ")
        self.date_entry = DateEntry(self, year=2023, month=11, day=30)

        time_label = custk.CTkLabel(self, text="Pick-up Time: ")
        self.time_combobox = custk.CTkComboBox(self, values=times, state="readonly",)

        quantity_label = custk.CTkLabel(self, text="Quantity: ")
        self.cake_slider = custk.CTkSlider(self, from_=1, to=10, command=sliding)
        self.cake_slider.set(1)
        cake_slider_label = custk.CTkLabel(self, text="")

        fname_label = custk.CTkLabel(self, text="First Name: ")
        self.fname_entry = custk.CTkEntry(self)
        
        save_button = custk.CTkButton(self, text="Save", command=self.save_to_cake_orders_database, border_width= 3, border_color= "black")

        # Place widgets
        cake_label.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.cake_combobox.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        date_label.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        self.date_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        time_label.grid(row=6, column=0, sticky="ew", padx=5, pady=5)
        self.time_combobox.grid(row=6, column=1, sticky="ew", padx=5, pady=5)

        quantity_label.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        self.cake_slider.grid(row=3, column=1, sticky="ew", padx=5, pady=(5, 0))
        cake_slider_label.grid(row=4, column=1, sticky="nsew", padx=5, pady=(0, 5))

        fname_label.grid(row=5, column=0, sticky="ew", padx=5, pady=5)
        self.fname_entry.grid(row=5, column=1, sticky="ew", padx=5, pady=5)
        
        save_button.grid(row=7, column=0, columnspan=4, sticky="nsew", pady=10)

    def save_to_cake_orders_database(self):
        cake_type = self.cake_combobox.get()
        date = self.date_entry.get()
        time = self.time_combobox.get()
        quantity = self.cake_slider.get()
        fname = self.fname_entry.get()

        if not all([cake_type, date, time, quantity, fname]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        conn = sqlite3.connect("cake_orders.db")
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS cake_orders
                          (cake_type TEXT, date TEXT, time TEXT, quantity INT, fname TEXT)''')

        cursor.execute("INSERT INTO cake_orders VALUES (?, ?, ?, ?, ?)", (cake_type, date, time, quantity, fname))

        conn.commit()
        conn.close()

        messagebox.showinfo("Order cake","Cake ordered!")
