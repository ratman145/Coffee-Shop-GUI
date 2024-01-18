import tkinter as tk
import customtkinter as custk
import sqlite3
from tkinter import messagebox

# Choose hamper
class ChooseHamper(custk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.label = custk.CTkLabel(self, text="Customize Hamper")
        self.label.grid(row=0, column=0, columnspan=4, sticky="nsew")

        self.items = ["Assorted Cakes", "Wine", "Varied Fruit", "Lancashire Cheese", "Brazil Nuts", "Scented Candle", "Tea Leaves", "Premium Coffee Beans"]

        self.hamper_widgets()

        # Configure column weights to make widgets stretch
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.grid_rowconfigure(10, weight=0)

    def hamper_widgets(self):
        sender_label = custk.CTkLabel(self, text="Sender's Name: ")
        self.sender_entry = custk.CTkEntry(self)

        recipient_label = custk.CTkLabel(self, text="Recipient's Name: ")
        self.recipient_entry = custk.CTkEntry(self)

        postcode_label = custk.CTkLabel(self, text="Recipient's Postcode: ")
        self.postcode_entry = custk.CTkEntry(self)

        items_label = custk.CTkLabel(self, text="Select Items: ")

        # Initialize IntVar instances for checkboxes
        self.selected_items = [tk.IntVar() for _ in self.items]

        for i, item in enumerate(self.items):
            checkbox = custk.CTkCheckBox(self, text=item, variable=self.selected_items[i])
            checkbox.grid(row=i + 2, column=0, sticky="w")

        save_button = custk.CTkButton(self, text="Save", command=self.save_to_hamper_order_database, border_width= 3, border_color= "black")

        # Place widgets
        sender_label.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        self.sender_entry.grid(row=2, column=2, sticky="ew", padx=5, pady=5)

        recipient_label.grid(row=3, column=1, sticky="ew", padx=5, pady=5)
        self.recipient_entry.grid(row=3, column=2, sticky="ew", padx=5, pady=5)

        postcode_label.grid(row=4, column=1, sticky="ew", padx=5, pady=5)
        self.postcode_entry.grid(row=4, column=2, sticky="ew", padx=5, pady=5)

        items_label.grid(row=1, column=0, sticky="ew", padx=5, pady=5, columnspan=2)

        save_button.grid(row=len(self.items) + 5, column=0, columnspan=4, sticky="nsew", pady=10)

    def save_to_hamper_order_database(self):
        sender_name = self.sender_entry.get()
        recipient_name = self.recipient_entry.get()
        recipient_postcode = self.postcode_entry.get()

        selected_items = [item for item, var in zip(self.items, self.selected_items) if var.get()]

        if not all([sender_name, recipient_name, recipient_postcode]):
            messagebox.showerror("Error", "Please fill in all required fields.")
            return
        
        if not sender_name.isalpha():
            messagebox.showerror("Error", "Please only use letters in field: Sender's Name")
            return
        
        if not recipient_name.isalpha():
            messagebox.showerror("Error", "Please only use letters in field: Recipient's Name")
            return

        conn = sqlite3.connect("hamper_order.db")
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS hampers (sender_name TEXT, recipient_name TEXT, recipient_postcode TEXT, items TEXT)''')

        cursor.execute("INSERT INTO hampers VALUES (?, ?, ?, ?)", (sender_name, recipient_name, recipient_postcode, ", ".join(selected_items)))

        conn.commit()
        conn.close()

        messagebox.showinfo("Create a hamper","Hamper Ordered!")