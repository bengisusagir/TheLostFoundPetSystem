import tkinter as tk
from tkinter import StringVar, ttk, messagebox, Entry
import sqlite3
import sys
import os
from new_report_page import ReportApp
from my_reports_page import MyReportsPage
from report_details_page import ReportDetails

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import dblib

class AllReportsPage(tk.Tk):
    def __init__(self,user):
        super().__init__()
        self.title("Lost & Found Pet System - All Reports")
        self.geometry("1000x600")
        self.resizable(False, False)
        self.db = dblib.LostFoundDatabase()
        self.editable = False
        self.user = user
        self.user_id = user[0]
        
        
        self.create_menu()
        self.create_table_layout()
        
    def create_menu(self):
        # Üst menü çubuğu
        menu_frame = tk.Frame(self, bg="lightgray", height=50)
        menu_frame.pack(fill="x")

        # Menü Butonları
        if(self.editable == False):
            tk.Button(menu_frame, text="New Report", command=self.new_report).pack(side="left", padx=10, pady=10)
            tk.Button(menu_frame, text="My Reports", command=self.my_reports).pack(side="left", padx=10)
            tk.Button(menu_frame, text="All Reports", relief="sunken", command=self.all_reports).pack(side="left", padx=10)  # Seçili buton
            tk.Button(menu_frame, text="TR / EN", command=self.change_language).pack(side="left", padx=10)
        else:
            tk.Button(menu_frame, text="New Report", command=self.new_report).pack(side="left", padx=10, pady=10)
            tk.Button(menu_frame, text="My Reports", relief="sunken", command=self.my_reports).pack(side="left", padx=10)  # Seçili buton
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
        
        # Ana sayfa içerik bölgesi
        content_frame = tk.Frame(self)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # 5 sütunlu grid yapısı
        for i in range(5):
            content_frame.columnconfigure(i, weight=1)
        
        # Boş 1. Sütun
        tk.Label(content_frame, text="", bg="white").grid(row=0, column=0, sticky="nsew")
    

        if(self.editable == False):
            reportInfo = self.db.get_reports()
        else:
            reportInfo = self.db.get_reports_by_user(self.user_id)

        rowNumber = 0
        
        for report in reportInfo:
            # İlan Detayları
            
            
            tk.Label(content_frame, text=f"Name: {report[2]}", font=("Arial", 12)).grid(row=rowNumber, column=1, sticky="w", padx=10, pady=5)
            tk.Label(content_frame, text=f"Type: {report[3]}", font=("Arial", 12)).grid(row=rowNumber + 1, column=1, sticky="w", padx=10, pady=5)
            tk.Label(content_frame, text=f"Location: {report[4]}", font=("Arial", 12)).grid(row=rowNumber, column=2, sticky="w", padx=10, pady=5)
            tk.Button(content_frame, text="Details", command=lambda r=report[0]: self.report_details(r)).grid(row=rowNumber + 1, column=2, sticky="w", padx=10, pady=5)
            if(self.editable == True):
                tk.Button(content_frame, text="Delete", command=lambda r=report[0]: self.delete_report(r)).grid(row=rowNumber + 1, column=2, sticky="w", padx=70, pady=5)
            

            # Fotoğraf Yer Tutucu
            tk.Label(content_frame, text=report[6], bg="gray", width=20, height=5).grid(row=rowNumber, column=3, rowspan=2, sticky="nsew", padx=10, pady=5)

            # Çizgi (Separator)
            separator = ttk.Separator(content_frame, orient="horizontal")
            separator.grid(row=rowNumber + 3, column=1, columnspan=3, sticky="ew", pady=5)
            
            rowNumber += 4


            # Boş 5. Sütun
            tk.Label(content_frame, text="", bg="white").grid(row=0, column=4, sticky="nsew")
            
        
    # Menü İşlevleri
    def new_report(self):
        new_report_window = tk.Toplevel(self)
        ReportApp(new_report_window,self.user_id)
        
    def my_reports(self):
        self.reset_page()
        self.editable = True
        
        self.create_menu()
        self.create_table_layout()
        

    def change_language(self):
        messagebox.showinfo("Language", "Change language to TR/EN")

    def edit_user(self):
        # Yeni pencere oluştur
        edit_user_window = tk.Toplevel(self)
        edit_user_window.title("Edit User")
        edit_user_window.geometry("300x250")

        # Kullanıcı bilgileri için alanlar
        tk.Label(edit_user_window, text="Username:").pack(pady=5)
        self.username_var = StringVar(value=self.user[1])
        self.username_entry = Entry(edit_user_window, textvariable=self.username_var, width=40)
        self.username_entry.pack()
        


        

    def delete_user(self,user_id):
        if messagebox.askyesno("Delete User", "Are you sure you want to delete your account?"):
            messagebox.showinfo("Delete User", "User account deleted")
            self.db.delete_user(user_id)

    def reset_page(self):
        for widget in self.winfo_children():
            widget.destroy()
        
    def all_reports(self):
        self.reset_page()
        self.editable = False
        self.create_menu()
        self.create_table_layout()

    def report_details(self,report_id):
        report_details_window = tk.Toplevel(self)
        ReportDetails(report_details_window,report_id,self.editable)
        
    def delete_report(self,report_id):
        if messagebox.askyesno("Delete User", "Are you sure you want to delete your account?"):
            self.db.delete_report(report_id)
            self.reset_page()
            self.create_menu()
            self.create_table_layout()
        
if __name__ == "__main__":
    app = AllReportsPage()
    app.mainloop()