import tkinter as tk
from tkinter import StringVar, ttk, messagebox
import sqlite3
import sys
import os
from new_report_page import ReportApp

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import dblib

class AllReportsPage(tk.Tk):
    def __init__(self,user_id):
        super().__init__()
        self.title("Lost & Found Pet System - All Reports")
        self.geometry("1000x600")
        self.resizable(False, False)
        self.db = dblib.LostFoundDatabase()
        self.user_id = StringVar(value=user_id)
        self.create_menu()
        self.create_table_layout()

    def create_menu(self):
        # Üst menü çubuğu
        menu_frame = tk.Frame(self, bg="lightgray", height=50)
        menu_frame.pack(fill="x")

        # Menü Butonları
        tk.Button(menu_frame, text="New Report", command=self.new_report).pack(side="left", padx=10, pady=10)
        tk.Button(menu_frame, text="My Reports", command=self.my_reports).pack(side="left", padx=10)
        tk.Button(menu_frame, text="All Reports", relief="sunken").pack(side="left", padx=10)  # Seçili buton
        tk.Button(menu_frame, text="TR / EN", command=self.change_language).pack(side="left", padx=10)

        # Profile Dropdown Menü
        profile_menu = ttk.Menubutton(menu_frame, text="Profile", direction="below")
        profile_dropdown = tk.Menu(profile_menu, tearoff=0)
        profile_dropdown.add_command(label="Edit User", command=self.edit_user)
        profile_dropdown.add_command(label="Delete User", command=self.delete_user)
        profile_menu["menu"] = profile_dropdown
        profile_menu.pack(side="right", padx=10)

    
    def create_table_layout(self):
        # Ana sayfa içerik bölgesi
        content_frame = tk.Frame(self)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # 5 sütunlu grid yapısı
        for i in range(5):
            content_frame.columnconfigure(i, weight=1)

        # Boş 1. Sütun
        tk.Label(content_frame, text="", bg="white").grid(row=0, column=0, sticky="nsew")
    

        row_num = 1  # Satır başlatma
        reportInfo = self.db.get_reports()
      
        for report in reportInfo:
            # İlan Detayları
            tk.Label(content_frame, text=f"Name: {report[2]}", font=("Arial", 12)).grid(row=row_num, column=1, sticky="w", padx=10, pady=5)
            tk.Label(content_frame, text=f"Type: {report[3]}", font=("Arial", 12)).grid(row=row_num, column=2, sticky="w", padx=10, pady=5)
            tk.Label(content_frame, text=f"Location: {report[4]}", font=("Arial", 12)).grid(row=row_num + 1, column=1, sticky="w", padx=10, pady=5)
            tk.Label(content_frame, text=f"Description: {report[5]}", font=("Arial", 12)).grid(row=row_num + 1, column=2, sticky="w", padx=10, pady=5)

            # Fotoğraf Yer Tutucu
            tk.Label(content_frame, text=report[6], bg="gray", width=20, height=5).grid(row=row_num, column=3, rowspan=2, sticky="nsew", padx=10, pady=5)

            # Çizgi (Separator)
            separator = ttk.Separator(content_frame, orient="horizontal")
            separator.grid(row=row_num + 2, column=1, columnspan=3, sticky="ew", pady=5)

            row_num += 3  # Yeni ilan için satırı kaydır

        # Boş 5. Sütun
        tk.Label(content_frame, text="", bg="white").grid(row=0, column=4, sticky="nsew")

    # Menü İşlevleri
    def new_report(self):
        new_report_window = tk.Toplevel(self)
        ReportApp(new_report_window,self.user_id)
        
    def my_reports(self):
        messagebox.showinfo("My Reports", "Navigate to My Reports Page")

    def change_language(self):
        messagebox.showinfo("Language", "Change language to TR/EN")

    def edit_user(self):
        messagebox.showinfo("Edit User", "Edit user details")

    def delete_user(self):
        if messagebox.askyesno("Delete User", "Are you sure you want to delete your account?"):
            messagebox.showinfo("Delete User", "User account deleted")

if __name__ == "__main__":
    app = AllReportsPage()
    app.mainloop()