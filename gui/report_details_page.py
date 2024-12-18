import sqlite3
from tkinter import Tk, Label, Button, Entry, StringVar, filedialog, messagebox, ttk
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import dblib

class ReportDetails:
    def __init__(self, root, report_id, editable=False):
        self.root = root
        self.editable = editable
        
        self.root.title("Report Details")
        self.root.geometry("600x400") 
        self.root.resizable(False, False) 
        self.root.configure(bg="lightblue") 
        
        self.db_name = "dblib.db" 
        self.db = dblib.LostFoundDatabase() 
        
        self.report_id = report_id
        report = self.db.get_reportdetails(self.report_id)
        
        if report:
            Label(self.root, text="Report Details", font=("Arial", 18, "bold"), bg="lightblue").grid(row=0, column=0, columnspan=3, pady=10)

            Label(self.root, text="Pet Name:", bg="lightblue", anchor="w").grid(row=1, column=0, padx=10, pady=5, sticky="w")
            Label(self.root, text="Pet Type:", bg="lightblue", anchor="w").grid(row=2, column=0, padx=10, pady=5, sticky="w")
            Label(self.root, text="Location:", bg="lightblue", anchor="w").grid(row=3, column=0, padx=10, pady=5, sticky="w")
            Label(self.root, text="Description:", bg="lightblue", anchor="nw").grid(row=4, column=0, padx=10, pady=5, sticky="nw")
            Label(self.root, text="Photo:", bg="lightblue", anchor="w").grid(row=5, column=0, padx=10, pady=5, sticky="w")

            if self.editable:
                self.pet_name_var = StringVar(value=report[0][2])
                self.pet_name_entry = Entry(self.root, textvariable=self.pet_name_var, width=40)
                self.pet_name_entry.grid(row=1, column=1, padx=10, pady=5)
                
                self.pet_type_var = StringVar(value=report[0][3])
                self.pet_type_entry = Entry(self.root, textvariable=self.pet_type_var, width=40)
                self.pet_type_entry.grid(row=2, column=1, padx=10, pady=5)

                self.location_var = StringVar(value=report[0][4])
                self.location_entry = Entry(self.root, textvariable=self.location_var, width=40)
                self.location_entry.grid(row=3, column=1, padx=10, pady=5)
                
                self.description_var = StringVar(value=report[0][5])
                self.description_entry = Entry(self.root, textvariable=self.description_var, width=40)
                self.description_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")
                
                self.photo_path_var = StringVar(value=report[0][6])
                self.photo_entry = Entry(self.root, textvariable=self.photo_path_var, width=40, state="readonly")
                self.photo_entry.grid(row=5, column=1, padx=10, pady=5)
                Button(self.root, text="Browse", command=self.browse_file).grid(row=5, column=2, padx=10, pady=5)
                Button(self.root, text="Save", command=self.save_report, bg="green", fg="white", width=15).grid(row=6, column=1, pady=20, sticky="e")
                
            else:
                Label(self.root, text=report[0][2], bg="lightblue", anchor="w").grid(row=1, column=1, padx=10, pady=5, sticky="w")
                Label(self.root, text=report[0][3], bg="lightblue", anchor="w").grid(row=2, column=1, padx=10, pady=5, sticky="w")
                Label(self.root, text=report[0][4], bg="lightblue", anchor="w").grid(row=3, column=1, padx=10, pady=5, sticky="w")
                Label(self.root, text=report[0][5], bg="lightblue", wraplength=400, justify="left").grid(row=4, column=1, padx=10, pady=5, sticky="w")
                Label(self.root, text=os.path.basename(report[0][6]), bg="lightblue", anchor="w").grid(row=5, column=1, padx=10, pady=5, sticky="w")
            
        else:
            messagebox.showerror("Error", "Report not found or is incomplete")
            self.root.destroy()

    def browse_file(self):
        file_path = filedialog.askopenfilename(title="Select Photo", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            self.photo_path_var.set(file_path)

    def save_report(self):
        pet_name = self.pet_name_var.get()
        pet_type = self.pet_type_var.get()
        location = self.location_var.get()
        description = self.description_var.get()
        photo_path = self.photo_path_var.get()

        self.db.update_report(self.report_id, pet_name, pet_type, location, description, photo_path)
        messagebox.showinfo("Success", "Report updated successfully!")

if __name__ == "__main__":
    root = Tk()
    root.mainloop()