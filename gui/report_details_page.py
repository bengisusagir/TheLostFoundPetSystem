import shutil
import sqlite3
from tkinter import Image, OptionMenu, Text, Tk, Label, Button, Entry, StringVar, filedialog, messagebox, ttk
from tkinter import ttk  # Import ttk for the style
from tkinter import PhotoImage 
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import dblib
from languages import LANGUAGES 

class ReportDetails:
    def __init__(self, root, report_id, editable=False,language=""):
        self.root = root
        self.editable = editable
        self.languageNo = 0 if language == "en" else 1
        self.root.title(LANGUAGES["report_details"][self.languageNo])
        
        self.db_name = "dblib.db" 
        self.db = dblib.LostFoundDatabase() 
        
        self.report_id = report_id
        report = self.db.get_reportdetails(self.report_id)

        
        if report:
            Label(root, text=LANGUAGES["report_details"][self.languageNo], font=("Arial", 16, "bold"), bg="#4CAF50", fg="white", anchor="center").grid(row=0, column=0, columnspan=3, padx=5, pady=20, sticky="nsew")
            Label(self.root, text=LANGUAGES["pet_name"][self.languageNo], font=("Arial", 12), bg="#f0f0f0", anchor="w").grid(row=1, column=0, padx=10, pady=5, sticky="w")
            Label(self.root, text=LANGUAGES["pet_type"][self.languageNo], font=("Arial", 12), bg="#f0f0f0", anchor="w").grid(row=2, column=0, padx=10, pady=5, sticky="w")
            Label(self.root, text=LANGUAGES["location"][self.languageNo], font=("Arial", 12), bg="#f0f0f0", anchor="w").grid(row=3, column=0, padx=10, pady=5, sticky="w")
            Label(root, text=LANGUAGES["description"][self.languageNo], font=("Arial", 12), bg="#f0f0f0", anchor="nw").grid(row=4, column=0, padx=10, pady=5, sticky="nw")
            

            Label(self.root, text=LANGUAGES["photo"][self.languageNo], font=("Arial", 12), bg="#f0f0f0", anchor="w").grid(row=6, column=0, padx=10, pady=5, sticky="w")

            if self.editable:
                self.pet_name_var = StringVar(value=report[0][2])
                self.pet_name_entry = Entry(self.root, textvariable=self.pet_name_var, font=("Arial", 12), width=40, relief="solid")
                self.pet_name_entry.grid(row=1, column=1, padx=10, pady=5)
                
                self.pet_types = [LANGUAGES["cat"][self.languageNo], LANGUAGES["dog"][self.languageNo], LANGUAGES["bird"][self.languageNo], LANGUAGES["other"][self.languageNo]]
                self.pet_type_var = StringVar(value=report[0][3])
                self.pet_type_entry = OptionMenu(self.root, self.pet_type_var, *self.pet_types)
                self.pet_type_entry.config(font=("Arial", 12),anchor="w")
                self.pet_type_entry.grid(row=2, column=1, padx=10, pady=5)

                self.location_var = StringVar(value=report[0][4])
                self.location_entry = Entry(self.root, textvariable=self.location_var, font=("Arial", 12), width=40, relief="solid")
                self.location_entry.grid(row=3, column=1, padx=10, pady=5)
                
                self.description_var = StringVar(value=report[0][5])
                self.description_entry = Text(root, width=40, height=5, font=("Arial", 12), bg="white", fg="black", wrap="word", relief="solid")
                self.description_entry.insert("1.0", report[0][5])
                self.description_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

                
                self.photo_path_var = StringVar(value=report[0][6])
                self.photo_entry = Entry(self.root, textvariable=self.photo_path_var, font=("Arial", 12), width=40, state="readonly", relief="solid")
                self.photo_entry.grid(row=6, column=1, padx=10, pady=5)
                
                Button(self.root, text=LANGUAGES["browse"][self.languageNo], command=self.browse_file, bg="#4CAF50", fg="white", font=("Arial", 12), width=15).grid(row=6, column=2, padx=10, pady=5)

                Button(self.root, text=LANGUAGES["save"][self.languageNo], command=self.save_report, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), width=15).grid(row=8, column=2, pady=20, sticky="w")
                
                self.display_image(report[0][6])

            else:
                Label(self.root, text=report[0][2], font=("Arial", 12), anchor="w").grid(row=1, column=1, padx=10, pady=5, sticky="w")
                Label(self.root, text=report[0][3],  font=("Arial", 12), anchor="w").grid(row=2, column=1, padx=10, pady=5, sticky="w")
                Label(self.root, text=report[0][4],  font=("Arial", 12), anchor="w").grid(row=3, column=1, padx=10, pady=5, sticky="w")
                Label(self.root, text=report[0][5], font=("Arial", 12), wraplength=400, justify="left").grid(row=4, column=1, padx=10, pady=5, sticky="w")
                Label(self.root, text=os.path.basename(report[0][6]), font=("Arial", 12), anchor="w").grid(row=6, column=1, padx=10, pady=5, sticky="w")
                self.display_image(report[0][6])
        else:
            messagebox.showerror("Error", LANGUAGES["report_not_found"][self.languageNo])
            self.root.destroy()
    

    def display_image(self, photo_path):
        try:
            if os.path.exists(photo_path):
                # PhotoImage only supports .png
                image = PhotoImage(file=photo_path)
                img_width, img_height = image.width(), image.height()
                max_width, max_height = 200, 200
                scale = min(max_width / img_width, max_height / img_height, 1)
                new_width = int(img_width * scale)
                new_height = int(img_height * scale)

                resized_image = image.subsample(img_width // new_width, img_height // new_height)

                image_label = Label(self.root, image=resized_image)
                image_label.grid(row=7, column=1, padx=10, pady=10)
                image_label.image = resized_image 
            else:
                messagebox.showerror(
                LANGUAGES["error"][self.languageNo],
                LANGUAGES["image_not_found"][self.languageNo]
            )
        except Exception as e:
            messagebox.showerror(
            LANGUAGES["error"][self.languageNo],
            f"{LANGUAGES['failed_to_load_image'][self.languageNo]}: {str(e)}"
        )

        
    def browse_file(self):
        file_path = filedialog.askopenfilename(title="Select Photo", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            target_dir = "./assests/images"  
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            try:
                file_name = os.path.basename(file_path)
                new_file_path = os.path.join(target_dir, file_name)
                shutil.copy(file_path, new_file_path)  

                self.photo_path_var.set(new_file_path)
            except Exception as e:
                 messagebox.showerror(
                LANGUAGES["error"][self.languageNo],
                f"{LANGUAGES['failed_to_copy_photo'][self.languageNo]}: {str(e)}"
            )


    def save_report(self):
        pet_name = self.pet_name_var.get()
        pet_type = self.pet_type_var.get()
        location = self.location_var.get()
        description = self.description_entry.get("1.0", "end-1c")
        photo_path = self.photo_path_var.get()

        self.db.update_report(self.report_id, pet_name, pet_type, location, description, photo_path)
        messagebox.showinfo(
        LANGUAGES["success"][self.languageNo],
        LANGUAGES["report_updated_successfully"][self.languageNo]
    )
        self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    #report_id = 5
    #editable = True  
    #ReportDetails(root, report_id, editable,"tr")
    root.mainloop()