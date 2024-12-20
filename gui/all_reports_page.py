import re
import tkinter as tk
from tkinter import Label, PhotoImage, StringVar, ttk, messagebox, Entry
import sqlite3
import sys
import os
from new_report_page import ReportApp
from report_details_page import ReportDetails

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import dblib
from languages import LANGUAGES
class AllReportsPage(tk.Tk):
    def __init__(self,user,languageTag):
        super().__init__()
        self.languageNo = 0 if languageTag == "en" else 1
        self.title(LANGUAGES["titleAllReports"][self.languageNo])
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
            tk.Button(menu_frame, text=LANGUAGES["new_report"][self.languageNo], command=self.new_report).pack(side="left", padx=10, pady=10)
            tk.Button(menu_frame, text=LANGUAGES["my_reports"][self.languageNo], command=self.my_reports).pack(side="left", padx=10)
            tk.Button(menu_frame, text=LANGUAGES["all_reports"][self.languageNo], relief="sunken", command=self.all_reports).pack(side="left", padx=10)  # Seçili buton
            tk.Button(menu_frame, text=LANGUAGES["change_language"][self.languageNo], command=lambda: self.change_language(self.languageNo)).pack(side="left", padx=10)
        else:
            tk.Button(menu_frame, text=LANGUAGES["new_report"][self.languageNo], command=self.new_report).pack(side="left", padx=10, pady=10)
            tk.Button(menu_frame, text=LANGUAGES["my_reports"][self.languageNo], relief="sunken", command=self.my_reports).pack(side="left", padx=10)  # Seçili buton
            tk.Button(menu_frame, text=LANGUAGES["all_reports"][self.languageNo], command=self.all_reports).pack(side="left", padx=10)
            tk.Button(menu_frame, text=LANGUAGES["change_language"][self.languageNo], command=lambda: self.change_language(self.languageNo)).pack(side="left", padx=10)
        

        # Profile Dropdown Menü
        profile_menu = ttk.Menubutton(menu_frame, text=LANGUAGES["profile"][self.languageNo], direction="below")
        profile_dropdown = tk.Menu(profile_menu, tearoff=0)
        profile_dropdown.add_command(label=LANGUAGES["edit_user"][self.languageNo], command=lambda: self.edit_user(self.user[0]))
        profile_dropdown.add_command(label=LANGUAGES["delete_user"][self.languageNo], command=lambda: self.delete_user(self.user[0]))
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
            
            
            tk.Label(content_frame, text=f"{LANGUAGES["pet_name"][self.languageNo]}: {report[2]}", font=("Arial", 12)).grid(row=rowNumber, column=1, sticky="w", padx=10, pady=5)
            tk.Label(content_frame, text=f"{LANGUAGES["pet_type"][self.languageNo]}: {report[3]}", font=("Arial", 12)).grid(row=rowNumber + 1, column=1, sticky="w", padx=10, pady=5)
            tk.Label(content_frame, text=f"{LANGUAGES["location"][self.languageNo]}: {report[4]}", font=("Arial", 12)).grid(row=rowNumber, column=2, sticky="w", padx=10, pady=5)
            tk.Button(content_frame, text=f"{LANGUAGES["details_report"][self.languageNo]}", command=lambda r=report[0]: self.report_details(r)).grid(row=rowNumber + 1, column=2, sticky="w", padx=10, pady=5)
            if(self.editable == True):
                tk.Button(content_frame, text=f"{LANGUAGES["delete_report"][self.languageNo]}", command=lambda r=report[0]: self.delete_report(r)).grid(row=rowNumber + 1, column=2, sticky="w", padx=70, pady=5)
            

            # Fotoğraf Yer Tutucu
            photo_path = report[6]  # Resim yolu
            photo_label = self.display_image(content_frame, photo_path)  # Resmi içeren bir Label oluşturur
            photo_label.grid(row=rowNumber, column=3, rowspan=2, sticky="nsew", padx=10, pady=5)

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
        

    def change_language(self,languageNo):
        if(languageNo == 0):
            self.languageNo = 1
            self.reset_page()
            self.title(LANGUAGES["titleAllReports"][self.languageNo])
            self.create_menu()
            self.create_table_layout()
        else:
            self.languageNo = 0
            self.reset_page()
            self.title(LANGUAGES["titleAllReports"][self.languageNo])
            self.create_menu()
            self.create_table_layout()

    def edit_user(self, user_id):
        # Yeni pencere oluştur
        edit_user_window = tk.Toplevel(self)
        edit_user_window.title({LANGUAGES["edit_user"][self.languageNo]})
        edit_user_window.geometry("300x250")

        # Kullanıcı bilgileri için alanlar
        tk.Label(edit_user_window, text= LANGUAGES["username"][self.languageNo]).pack(pady=5)
        self.username_var = StringVar(value=self.user[1])
        self.username_entry = Entry(edit_user_window, textvariable=self.username_var, width=40)
        self.username_entry.pack()

        tk.Label(edit_user_window, text=LANGUAGES["password"][self.languageNo]).pack(pady=5)
        self.password_var = StringVar(value=self.user[2])
        self.password_entry = Entry(edit_user_window, textvariable=self.password_var, width=40)
        self.password_entry.pack()

        tk.Label(edit_user_window, text=LANGUAGES["phoneNo"][self.languageNo]).pack(pady=5)
        self.phoneNo_var = StringVar(value=self.user[3])
        self.phoneNo_entry = Entry(edit_user_window, textvariable=self.phoneNo_var, width=40)
        self.phoneNo_entry.pack()
        
        tk.Button(edit_user_window, text=LANGUAGES["save"][self.languageNo], command=self.save_user, bg="green", fg="white", width=15).pack(pady=10)
        
    def save_user(self):


        username = self.username_var.get()
        password = self.password_var.get()
        phoneNo = self.phoneNo_var.get()

        if(username == "" or password == "" or phoneNo == ""):
            messagebox.showerror(LANGUAGES["error"][self.languageNo], LANGUAGES["fillDataError"][self.languageNo])
            return
        

        if(self.checkEditInfo(username,password,phoneNo)):
            self.db.update_user(self.user_id,username,password,phoneNo)
            messagebox.showinfo(LANGUAGES["success"][self.languageNo], LANGUAGES["userUptaded"][self.languageNo])
            self.user = [self.user_id, username, password, phoneNo]

        return
        
        
        
        

        

    def delete_user(self,user_id):
        if messagebox.askyesno(LANGUAGES["delete_user"][self.languageNo], LANGUAGES["askDeleteUser"][self.languageNo]):
            self.db.delete_user(user_id)
            self.db.deleteAllReports(user_id)
            messagebox.showinfo(LANGUAGES["delete_user"][self.languageNo], LANGUAGES["userDeleted"][self.languageNo])
            self.destroy()
            

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
        if messagebox.askyesno(LANGUAGES["deleteTheReport"][self.languageNo], LANGUAGES["askDeleteReport"][self.languageNo]):
            self.db.delete_report(report_id)
            self.reset_page()
            self.create_menu()
            self.create_table_layout()
            
    def checkEditInfo(self,username,password,phoneNo):
            
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

            if not(len(phoneNo) == 10 and not phoneNo.isdigit()):
                messagebox.showerror(LANGUAGES["error"][self.languageNo], LANGUAGES["validPhone"][self.languageNo])
                return False
            
            return True
        
            

        
    def display_image(self, parent, photo_path):
        try:
            if os.path.exists(photo_path):
                image = PhotoImage(file=photo_path)
                img_width, img_height = image.width(), image.height()
                max_width, max_height = 200, 200
                scale = min(max_width / img_width, max_height / img_height, 1)
                new_width = int(img_width * scale)
                new_height = int(img_height * scale)

                resized_image = image.subsample(img_width // new_width, img_height // new_height)

                image_label = Label(parent, image=resized_image)
                image_label.image = resized_image  # bunu koymazsak image gozukmuyo

                return image_label
            else:
                messagebox.showerror(LANGUAGES["error"][self.languageNo], LANGUAGES["imageNotFound"][self.languageNo])
                return Label(parent, text="No Image", bg="gray", width=20, height=5)
        except Exception as e:
            messagebox.showerror(LANGUAGES["error"][self.languageNo], LANGUAGES["failedImage"][self.languageNo] + str(e))
            return
        
        
if __name__ == "__main__":
    app = AllReportsPage()
    app.mainloop()