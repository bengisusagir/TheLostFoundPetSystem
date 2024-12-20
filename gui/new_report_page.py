import shutil
import sqlite3
from tkinter import OptionMenu, Tk, Label, Entry, Button, Text, Toplevel, filedialog, StringVar, messagebox
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from languages import LANGUAGES
import dblib

class ReportApp:
    def __init__(self, root, user_id,language):
        self.root = root
        print("language",language)
        self.languageNo = 0 if language == "en" else 1
        self.root.title("New Report Page")
        self.root.title(LANGUAGES["new_rep_title"][self.languageNo])
        self.db_name = "dblib.db"  
        self.db = dblib.LostFoundDatabase()
        self.user_id = user_id
        self.pet_name = StringVar()
        self.pet_type = StringVar()
        self.location = StringVar()
        self.photo_path = StringVar()

        self.pet_types = [LANGUAGES["cat"][self.languageNo],LANGUAGES["dog"][self.languageNo], LANGUAGES["bird"][self.languageNo], LANGUAGES["other"][self.languageNo]] 
        self.pet_type.set(self.pet_types[0]) 
        
        Label(root, text=LANGUAGES["new_rep_title"][self.languageNo], font=("Arial", 16, "bold"), bg="#4CAF50", fg="white", anchor="center").grid(row=0, column=0, columnspan=3, padx=10, pady=20, sticky="nsew")

        
        Label(root, text=LANGUAGES["pet_name"][self.languageNo], font=("Arial", 12), bg="#f0f0f0", anchor="w").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        entry = Entry(root, textvariable=self.pet_name, font=("Arial", 12), bg="white", fg="black", relief="solid", width=40)
        entry.grid(row=1, column=1, padx=10, pady=5)

        Label(root, text=LANGUAGES["pet_type"][self.languageNo], font=("Arial", 12), bg="#f0f0f0", anchor="w").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        OptionMenu(root, self.pet_type, *self.pet_types).grid(row=2, column=1, padx=10, pady=5)

        Label(root, text=LANGUAGES["location"][self.languageNo], font=("Arial", 12), bg="#f0f0f0", anchor="w").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        entry = Entry(root, textvariable=self.location, font=("Arial", 12), bg="white", fg="black", relief="solid", width=40)
        entry.grid(row=4, column=1, padx=10, pady=5)

        Label(root, text=LANGUAGES["description"][self.languageNo], font=("Arial", 12), bg="#f0f0f0", anchor="nw").grid(row=5, column=0, padx=10, pady=5, sticky="nw")
        self.description_text = Text(root, width=40, height=5, font=("Arial", 12), bg="white", fg="black", wrap="word", relief="solid")
        self.description_text.grid(row=5, column=1, padx=10, pady=5)

        Label(root, text=LANGUAGES["photo_path"][self.languageNo], font=("Arial", 12), bg="#f0f0f0").grid(row=6, column=0, padx=10, pady=5, sticky="w")
        Entry(root, textvariable=self.photo_path, state="readonly", font=("Arial", 12), bg="white", fg="black", relief="solid", width=40).grid(row=6, column=1, padx=10, pady=5)
        Button(root, text=LANGUAGES["browse"][self.languageNo], command=self.browse_file, bg="#4CAF50", fg="white", font=("Arial", 12), width=15).grid(row=6, column=2, padx=10, pady=5)

        Button(root, text=LANGUAGES["save_report"][self.languageNo], command=self.save_report, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), width=20).grid(row=7, column=1, pady=20)

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title=LANGUAGES["select_photo"][self.languageNo],
            filetypes=[(LANGUAGES["image_files"][self.languageNo], "*.jpg;*.jpeg;*.png")]
        )
        if file_path:
            target_dir = "./assets/images"
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            try:
                file_name = os.path.basename(file_path)
                new_file_path = os.path.join(target_dir, file_name)
                shutil.copy(file_path, new_file_path)

                self.photo_path.set(new_file_path)
            except Exception as e:
                messagebox.showerror(
                    LANGUAGES["error"][self.languageNo],
                    f"{LANGUAGES['failed_to_copy_photo'][self.languageNo]}: {str(e)}"
                )

    def save_report(self):
        pet_name = self.pet_name.get()
        pet_type = self.pet_type.get()
        location = self.location.get()
        description = self.description_text.get("1.0", "end-1c")
        photo_path = self.photo_path.get()

        if not (self.user_id and pet_name and pet_type and location and description and photo_path):
            messagebox.showerror(
                LANGUAGES["error"][self.languageNo],
                LANGUAGES["all_fields_required"][self.languageNo]
            )
            return

        try:
            self.db.save_report(self.user_id, pet_name, pet_type, location, description, photo_path)
            messagebox.showinfo(
                LANGUAGES["success"][self.languageNo],
                f"{LANGUAGES['report_saved'][self.languageNo]}, {pet_name}!"
            )
            self.root.destroy()

        except Exception as e:
            messagebox.showerror(
                LANGUAGES["error"][self.languageNo],
                f"Failed to save report: {str(e)}"
            )
if __name__ == "__main__":
    root = Tk()
    #user_id = 1
    #editable = True  
    #ReportApp(root, user_id)
    root.mainloop()