import tkinter as tk
from tkinter import messagebox
import sqlite3
import dblib

# Ana Uygulama Sınıfı
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lost & Found Pet System")
        self.geometry("400x300")
        self.resizable(False, False)
        self.show_login_page()
        self.db = dblib.LostFoundDatabase()

    def show_login_page(self):
        # Login sayfası
        for widget in self.winfo_children():
            widget.destroy()
        tk.Label(self, text="Login", font=("Arial", 20)).pack(pady=10)

        tk.Label(self, text="Username:").pack()
        username_entry = tk.Entry(self, width=30)
        username_entry.pack()

        tk.Label(self, text="Password:").pack()
        password_entry = tk.Entry(self, show="*", width=30)
        password_entry.pack()

        def login_action():
            username = username_entry.get()
            password = password_entry.get()
            user = self.db.get_userpass_by_username(username, password)
            if user:
                messagebox.showinfo("Success", f"Welcome, {username}!")
            else:
                messagebox.showerror("Error", "Invalid username or password.")      

        login_btn = tk.Button(self, text="Login", command=login_action)
        login_btn.pack(pady=5)

        tk.Button(self, text="Register", command=self.show_register_page).pack()

    def show_register_page(self):
        # Register sayfası
        for widget in self.winfo_children():
            widget.destroy()
        tk.Label(self, text="Register", font=("Arial", 20)).pack(pady=10)

        tk.Label(self, text="Username:").pack()
        username_entry = tk.Entry(self, width=30)
        username_entry.pack()

        tk.Label(self, text="Password:").pack()
        password_entry = tk.Entry(self, show="*", width=30)
        password_entry.pack()

        def register_action():
            username = username_entry.get()
            password = password_entry.get()
            if username and password:
                try:
                    self.db.save_user(username, password)
                    messagebox.showinfo("Success", "Registration successful!")
                    self.show_login_page()
                except sqlite3.IntegrityError:
                    messagebox.showerror("Error", "Username already exists.")
            else:
                messagebox.showwarning("Warning", "All fields are required!")

        tk.Button(self, text="Register", command=register_action).pack(pady=5)
        tk.Button(self, text="Back to Login", command=self.show_login_page).pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()