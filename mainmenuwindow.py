import customtkinter as custk
from booktablewindow import BookTable
from ordercoffeewindow import OrderCoffee
from booklessonwindow import BookLesson
from ordercakewindow import OrderCake
from choosehamperwindow import ChooseHamper
from createaccountwindow import CreateAccount
from sharewindow import ShareButton

custk.set_appearance_mode("dark")
custk.set_default_color_theme("green")
# Main window
class Window(custk.CTk):
    def __init__(self, title, size):
        super().__init__()
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self.minsize(size[0], size[1])

        self.menu = SideMenu(self)
        self.menu.grid(row=0, column=0, sticky="nsew")

        self.book = BookTable(self)
        self.book.grid(row=0, column=1, sticky="nsew")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)  # Allowing the first row to expand

        self.mainloop()

class SideMenu(custk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        custk.CTkLabel(self, text="Main Menu").grid(row=0, column=0, columnspan=2)

        buttons = [
            ("Book Table", BookTable),
            ("Order Coffee", OrderCoffee),
            ("Book Lesson", BookLesson),
            ("Order Cake", OrderCake),
            ("Hampers", ChooseHamper),
            ("Create Account", CreateAccount),
            ("Share!", ShareButton)
        ]

        for i, (button_text, target_class) in enumerate(buttons):
            button = custk.CTkButton(self, text=button_text, border_width= 3, border_color= "black",  command=lambda target=target_class: self.show_frame(target))
            button.grid(row=i+1, column=0, sticky="nsew")
            self.grid_rowconfigure(i+1, weight=1)

        self.grid_columnconfigure(0, weight=1)

    def show_frame(self, frame_class):
        new_frame = frame_class(self.master)
        new_frame.grid(row=0, column=1, sticky="nsew")