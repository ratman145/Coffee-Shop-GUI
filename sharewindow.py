import customtkinter as custk
from tkinter import messagebox

#share button
class ShareButton(custk.CTkButton):
    def __init__(self, parent):
        super().__init__(parent, text="Share", command=self.show_popup, border_width= 3, border_color= "black")

    def show_popup(self):
        messagebox.showinfo("Share", "Thank you for sharing!")