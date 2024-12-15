import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lost & Found Pet System")
        self.geometry("800x600")
        self.resizable(False, False)

        # Menü Barı
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Report")
        file_menu.add_command(label="My Reports")
        file_menu.add_command(label="All Reports")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="Menu", menu=file_menu)

        # Ana Sayfa Mesajı
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)
        welcome_label = ttk.Label(self.main_frame, text="Welcome to Lost & Found Pet System!", font=("Arial", 16))
        welcome_label.pack(pady=20)

if __name__ == "__main__":
    app = App()
    app.mainloop()