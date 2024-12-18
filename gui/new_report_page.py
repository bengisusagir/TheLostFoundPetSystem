import sqlite3
from tkinter import Tk, Label, Entry, Button, Text, Toplevel, filedialog, StringVar, messagebox
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import dblib

class ReportApp:
    def __init__(self, root, user_id):
        self.root = root
        self.root.title("New Report Page")
        self.db_name = "dblib.db"  
        self.db = dblib.LostFoundDatabase()
        self.user_id = StringVar(value=user_id)
        self.pet_name = StringVar()
        self.pet_type = StringVar()
        self.location = StringVar()
        self.photo_path = StringVar()
        print("welcome"+str(user_id))
        Label(root, text="Pet Name:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        Entry(root, textvariable=self.pet_name).grid(row=1, column=1, padx=10, pady=5)

        Label(root, text="Pet Type:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        Entry(root, textvariable=self.pet_type).grid(row=2, column=1, padx=10, pady=5)


        Label(root, text="Location:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        Entry(root, textvariable=self.location).grid(row=4, column=1, padx=10, pady=5)

        Label(root, text="Description:").grid(row=5, column=0, padx=10, pady=5, sticky="nw")
        self.description_text = Text(root, width=40, height=5)
        self.description_text.grid(row=5, column=1, padx=10, pady=5)

        Label(root, text="Photo Path:").grid(row=6, column=0, padx=10, pady=5, sticky="w")
        Entry(root, textvariable=self.photo_path, state="readonly").grid(row=6, column=1, padx=10, pady=5)
        Button(root, text="Browse", command=self.browse_file).grid(row=6, column=2, padx=10, pady=5)

        Button(root, text="Save Report", command=self.save_report).grid(row=7, column=1, pady=20)

    def browse_file(self):
        file_path = filedialog.askopenfilename(title="Select Photo", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            self.photo_path.set(file_path)

    def save_report(self):
        user_id = self.user_id.get()
        pet_name = self.pet_name.get()
        pet_type = self.pet_type.get()
        location = self.location.get()
        description = self.description_text.get("1.0", "end-1c")
        photo_path = self.photo_path.get()

        if not (user_id and pet_name and pet_type and location and description and photo_path):
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            self.db.save_report(user_id, pet_name, pet_type, location, description, photo_path)
            messagebox.showinfo("Success", f"Report Saved, {pet_name}!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save report: {str(e)}")

if __name__ == "__main__":
    root = Tk()
    app = ReportApp(root)
    root.mainloop()
