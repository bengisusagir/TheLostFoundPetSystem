import re
import tkinter as tk
from tkinter import messagebox
import sqlite3
import sys
import os
from all_reports_page import AllReportsPage


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import dblib 
from languages import LANGUAGES

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.language = "tr"
        self.languageNo = 0 if self.language == "en" else 1
        self.title(LANGUAGES["titleLogin"][self.languageNo])
        self.geometry("400x300")
        self.resizable(False, False)
        self.show_login_page()
        self.db = dblib.LostFoundDatabase()
    

    def show_login_page(self):
        for widget in self.winfo_children():
            widget.destroy()
        tk.Label(
            self,
            text=LANGUAGES["login"][self.languageNo],
            font=("Arial", 18, "bold"),
            bg="#4CAF50",
            fg="white",
            pady=10,
        ).pack(fill="x")

        frame = tk.Frame(self, padx=20, pady=10)
        frame.pack(expand=True)

        tk.Label(frame, text=LANGUAGES["username"][self.languageNo], font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
        username_entry = tk.Entry(frame, width=30)
        username_entry.grid(row=0, column=1, pady=5)

        tk.Label(frame, text=LANGUAGES["password"][self.languageNo], font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
        password_entry = tk.Entry(frame, show="*", width=30)
        password_entry.grid(row=1, column=1, pady=5)
        
        def login_action():
            self.db.get_users()
            username = username_entry.get()
            password = password_entry.get()
            user = self.db.get_userpass_by_username(username, password)
            
            if user:
                messagebox.showinfo(LANGUAGES["success"][self.languageNo], f"{LANGUAGES['welcome'][self.languageNo]} {username}")
                self.destroy()
                AllReportsPage(user, self.language)

            else:
                messagebox.showerror(LANGUAGES["error"][self.languageNo], LANGUAGES["invalidUsernameorPassword"][self.languageNo])

        tk.Button(frame, text=LANGUAGES["login"][self.languageNo], command=login_action, width=15, bg="#4CAF50", fg="white").grid(row=2, column=1, pady=10)
        tk.Button(frame, text=LANGUAGES["register"][self.languageNo], command=self.show_register_page, width=15).grid(row=3, column=1, pady=5)

        tk.Button(self, text=LANGUAGES["change_language"][self.languageNo], command=lambda: self.changeLanguage(self.languageNo), width=20).pack(side="bottom", pady=10)

    def checkNewUserInfo(self,username,password,phoneNo):
            
            if(4 <= len(username) <= 12):
                if(re.search("[!@#$%^&*()]",username)):
                    messagebox.showerror(LANGUAGES["error"][self.languageNo], LANGUAGES["validUsername"][self.languageNo])
                    return False
            else: 
                messagebox.showerror(LANGUAGES["error"][self.languageNo], LANGUAGES["usernameLength"][self.languageNo])
                return False
            if(8 <= len(password) <= 16):
                if (not re.search("[A-Z]", password) or not re.search("[a-z]", password) or not re.search("[0-9]", password) or re.search("[!@#$%^&*()]", password)):
                    messagebox.showerror(LANGUAGES["error"][self.languageNo], LANGUAGES["validPassword"][self.languageNo])
                    return False
            else: 
                messagebox.showerror(LANGUAGES["error"][self.languageNo], LANGUAGES["passwordLength"][self.languageNo])
                return False

            if not (len(phoneNo) == 10 and phoneNo.isdigit()):
                messagebox.showerror(LANGUAGES["error"][self.languageNo], LANGUAGES["validPhone"][self.languageNo])
                return False
            
            return True

    def show_register_page(self):
        for widget in self.winfo_children():
            widget.destroy()
        tk.Label(
            self,
            text=LANGUAGES["register"][self.languageNo],
            font=("Arial", 18, "bold"),
            bg="#4CAF50",
            fg="white",
            pady=10,
        ).pack(fill="x")

        frame = tk.Frame(self, padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(frame, text=LANGUAGES["username"][self.languageNo], font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
        username_entry = tk.Entry(frame, width=30)
        username_entry.grid(row=0, column=1, pady=5)

        tk.Label(frame, text=LANGUAGES["password"][self.languageNo], font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
        password_entry = tk.Entry(frame, show="*", width=30)
        password_entry.grid(row=1, column=1, pady=5)

        tk.Label(frame, text=LANGUAGES["phoneNo"][self.languageNo], font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=5)
        phoneNo_entry = tk.Entry(frame, width=30)
        phoneNo_entry.grid(row=2, column=1, pady=5)

        def register_action():
            username = username_entry.get() 
            password = password_entry.get()
            phoneNo = phoneNo_entry.get()
            if username and password:
                try:
                    if(self.checkNewUserInfo(username,password,phoneNo)):
                        self.db.save_user(username, password, phoneNo)
                        messagebox.showinfo(LANGUAGES["success"][self.languageNo], LANGUAGES["registersuccess"][self.languageNo])
                        self.show_login_page()
                except sqlite3.IntegrityError:
                    messagebox.showerror(LANGUAGES["error"][self.languageNo], LANGUAGES["usernameexists"][self.languageNo])
            else:
                messagebox.showwarning(LANGUAGES["warning"][self.languageNo], LANGUAGES["allfields"][self.languageNo])

        tk.Button(frame, text=LANGUAGES["register"][self.languageNo], command=register_action, width=15, bg="#4CAF50", fg="white").grid(row=3, column=1, pady=10)
        tk.Button(frame, text=LANGUAGES["backtoLogin"][self.languageNo], command=self.show_login_page, width=15).grid(row=4, column=1, pady=5)

    def changeLanguage(self,languageNo):
        if(languageNo == 0):
            self.language = "tr"
            self.languageNo = 0 if self.language == "en" else 1
            self.title(LANGUAGES["titleLogin"][self.languageNo])
            self.show_login_page()
        else:
            self.language = "en"
            self.languageNo = 0 if self.language == "en" else 1
            self.title(LANGUAGES["titleLogin"][self.languageNo])
            self.show_login_page()
            
if __name__ == "__main__":
    app = App()
    app.mainloop()