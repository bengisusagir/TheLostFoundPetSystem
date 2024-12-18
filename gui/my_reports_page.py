import tkinter as tk
from tkinter import StringVar, ttk, messagebox
import sqlite3
import sys
import os
from new_report_page import ReportApp


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import dblib

class MyReportsPage(tk.Toplevel):
    def __init__(self, parent, user_id):
        super().__init__(parent)
        self.title("Lost & Found Pet System - My Reports")
        self.geometry("1000x600")
        self.resizable(False, False)
        self.db = dblib.LostFoundDatabase()
        self.user_id = user_id

        self.create_menu()
        self.create_table_layout()

    def create_menu(self):
        # Menü çubuğu (All Reports ile aynı)
        menu_frame = tk.Frame(self, bg="lightgray", height=50)
        menu_frame.pack(fill="x")

        tk.Button(menu_frame, text="New Report", command=self.new_report).pack(side="left", padx=10, pady=10)
        tk.Button(menu_frame, text="My Reports", relief="sunken").pack(side="left", padx=10)  # Seçili buton
        tk.Button(menu_frame, text="All Reports", command=self.all_reports).pack(side="left", padx=10)
        tk.Button(menu_frame, text="TR / EN", command=self.change_language).pack(side="left", padx=10)

        # Profile Dropdown Menü
        profile_menu = ttk.Menubutton(menu_frame, text="Profile", direction="below")
        profile_dropdown = tk.Menu(profile_menu, tearoff=0)
        profile_dropdown.add_command(label="Edit User", command=self.edit_user)
        profile_dropdown.add_command(label="Delete User", command=self.delete_user)
        profile_menu["menu"] = profile_dropdown
        profile_menu.pack(side="right", padx=10)

    def create_table_layout(self):
        # İçerik alanı
        content_frame = tk.Frame(self)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Sütun ayarları
        for i in range(5):
            content_frame.columnconfigure(i, weight=1)

        row_num = 1
        reports = self.db.get_user_reports(self.user_id)  # Kullanıcıya ait ilanları al

        for report in reports:
            # Pet Name ve Pet Type (üst üste)
            tk.Label(content_frame, text=f"Name: {report[0]}", font=("Arial", 12)).grid(
                row=row_num, column=1, sticky="w", padx=10, pady=5
            )
            tk.Label(content_frame, text=f"Type: {report[1]}", font=("Arial", 12)).grid(
                row=row_num + 1, column=1, sticky="w", padx=10
            )

            # Location (Sağda, y-ekseni ortalanmış)
            tk.Label(content_frame, text=f"Location: {report[2]}", font=("Arial", 12)).grid(
                row=row_num, column=3, rowspan=2, sticky="nsew", padx=10, pady=5
            )

            # Details Butonu
            tk.Button(content_frame, text="Details", command=lambda r=report: self.view_details(r[3])).grid(
                row=row_num, column=4, sticky="e", padx=10, pady=5
            )

            row_num += 3  # Sonraki ilan için satırı kaydır

    def view_details(self, report_id):
        details = self.db.get_report_details(report_id)  # İlan detaylarını almak için bir metod
        messagebox.showinfo("Details", f"Description:\n{details['description']}")

    # Diğer menü işlevleri
    def new_report(self):
        ReportApp(self, self.user_id)  # New Report sayfasını açar

    def all_reports(self):
        from all_reports_page import AllReportsPage  # Lokal import
        AllReportsPage(self.user_id)

    def change_language(self):
        messagebox.showinfo("Language", "Change language to TR/EN")

    def edit_user(self):
        messagebox.showinfo("Edit User", "Edit user details")

    def delete_user(self):
        if messagebox.askyesno("Delete User", "Are you sure you want to delete your account?"):
            messagebox.showinfo("Delete User", "User account deleted")
