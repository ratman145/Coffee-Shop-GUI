import customtkinter as custk
import sqlite3
from tkinter import messagebox

#Create account
class CreateAccount(custk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.label = custk.CTkLabel(self, text="Create Account")
        self.label.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.create_account_widgets()

        # Configure column weights to make widgets stretch
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def create_account_widgets(self):
        first_name_label = custk.CTkLabel(self, text="First Name: ")
        self.first_name_entry = custk.CTkEntry(self)

        last_name_label = custk.CTkLabel(self, text="Last Name: ")
        self.last_name_entry = custk.CTkEntry(self)

        email_label = custk.CTkLabel(self, text="Email: ")
        self.email_entry = custk.CTkEntry(self)

        phone_label = custk.CTkLabel(self, text="Phone Number: ")
        self.phone_entry = custk.CTkEntry(self)

        postcode_label = custk.CTkLabel(self, text="Postcode: ")
        self.postcode_entry = custk.CTkEntry(self)

        save_button = custk.CTkButton(self, text="Save", command=self.save_to_account_details_database, border_width= 3, border_color= "black")

        # Place widgets
        first_name_label.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.first_name_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        last_name_label.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        self.last_name_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        email_label.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        self.email_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

        phone_label.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
        self.phone_entry.grid(row=4, column=1, sticky="ew", padx=5, pady=5)

        postcode_label.grid(row=5, column=0, sticky="ew", padx=5, pady=5)
        self.postcode_entry.grid(row=5, column=1, sticky="ew", padx=5, pady=5)

        save_button.grid(row=6, column=0, columnspan=2, sticky="nsew", pady=10)

    def save_to_account_details_database(self):
        fname = self.first_name_entry.get()
        lname = self.last_name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        postcode = self.postcode_entry.get()

        if not all([fname, lname, email, phone, postcode]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        if not fname.isalpha():
            messagebox.showerror("Error", "Please only use letters in field: First Name")
            return
        
        if not lname.isalpha():
            messagebox.showerror("Error", "Please only use letters in field: Last Name")
            return
        
        if not phone.isnumeric():
            messagebox.showerror("Error", "Please only use numbers in field: Phone Number")
            return

        conn = sqlite3.connect("account_details.db")
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS accounts
                          (first_name TEXT, last_name TEXT, email TEXT, phone TEXT, postcode TEXT)''')

        cursor.execute("INSERT INTO accounts VALUES (?, ?, ?, ?, ?)", (fname, lname, email, phone, postcode))

        conn.commit()
        conn.close()

        messagebox.showinfo("Create account","Account created!")