import customtkinter as custk
import sqlite3
from tkinter import messagebox

#Order Coffee
class OrderCoffee(custk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.label = custk.CTkLabel(self, text="Order Coffee")
        self.label.grid(row=0, column=0, columnspan=4, sticky="nsew")

        self.order_widgets()

        # Configure column weights to make widgets stretch
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

    def order_widgets(self):
        coffee_types = ["Espresso", "Latte", "Cappuccino", "Americano", "Mocha"]
        cream_milk_options = ["None", "Cream", "Milk", "Soy Milk", "Oat Milk"]
        sugar_options = ["None", "Brown Sugar", "White Sugar"]
        dining_options = ["Sit In","Take Away"]

        coffee_label = custk.CTkLabel(self, text="Coffee Type: ")
        self.coffee_combobox = custk.CTkComboBox(self, values=coffee_types, state="readonly")

        cream_milk_label = custk.CTkLabel(self, text="Cream/Milk: ")
        self.cream_milk_combobox = custk.CTkComboBox(self, values=cream_milk_options, state="readonly")

        sugar_label = custk.CTkLabel(self, text="Sugar: ")
        self.sugar_combobox = custk.CTkComboBox(self, values=sugar_options, state="readonly")

        dining_options_label = custk.CTkLabel(self, text= "Dining Option: ")
        self.dining_options_combobox = custk.CTkComboBox(self, values=dining_options, state="readonly")

        save_button = custk.CTkButton(self, text="Save", command=self.save_to_coffee_orders_database, border_width= 3, border_color= "black")

        # Place widgets
        coffee_label.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.coffee_combobox.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        cream_milk_label.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        self.cream_milk_combobox.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        sugar_label.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        self.sugar_combobox.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

        dining_options_label.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
        self.dining_options_combobox.grid(row=4, column=1, sticky="ew", padx=5, pady=5)

        save_button.grid(row=5, column=0, columnspan=4, sticky="nsew", pady=10)

    def save_to_coffee_orders_database(self):
        coffee_type = self.coffee_combobox.get()
        cream_milk = self.cream_milk_combobox.get()
        sugar = self.sugar_combobox.get()
        dining_option = self.dining_options_combobox.get()

        if not all([coffee_type, cream_milk, sugar, dining_option]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        conn = sqlite3.connect("coffee_orders.db")
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS coffee_orders
                          (coffee_type TEXT, cream_milk TEXT, sugar TEXT, dining_option TEXT)''')

        cursor.execute("INSERT INTO coffee_orders VALUES (?, ?, ?, ?)", (coffee_type, cream_milk, sugar, dining_option))

        conn.commit()
        conn.close()

        messagebox.showinfo("Order coffee","Order placed!")