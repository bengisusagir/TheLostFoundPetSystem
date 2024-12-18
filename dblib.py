import sqlite3

class LostFoundDatabase:

    def __init__(self, db_name="LostFound.db"):
        self.db_name = db_name

    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        cur.execute("""
                create table if not exists users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                phoneNo TEXT NOT NULL
                );
                """)
        cur.execute("""create table if not exists reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                pet_name TEXT NOT NULL,
                pet_type TEXT NOT NULL,
                location TEXT NOT NULL,
                description TEXT NOT NULL,
                photo_path TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            );""")
        conn.commit()
        conn.close()

    def save_user(self, username, password,phoneNo):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        cur.execute("insert into users (username, password,phoneNo) values (?, ?,?)", (username, password, phoneNo))
        conn.commit()
        conn.close()
        
    def save_report(self, user_id, pet_name, pet_type,location,description,photo_path):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        cur.execute("insert into reports (user_id, pet_name, pet_type,location,description,photo_path) values (?, ?,?,?,?,?)", (user_id, pet_name, pet_type,location,description,photo_path))
        conn.commit()
        conn.close()
        

    def get_users(self):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        cur.execute("select * from users")
        user_list = cur.fetchall()
        print(f"DEBUG: Data: {user_list}") 
        conn.close()

        return user_list

    
    def get_userpass_by_username(self, username, password):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
        user_id = cur.fetchone()
        conn.close()
        return user_id
    
    def get_reports(self):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        cur.execute("select * from reports")
        report_list = cur.fetchall()
        conn.close()
        return report_list
        
    def get_reportdetails(self,report_id):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        cur.execute("select * from reports where report_id= ?")
        reportdetails = cur.fetchall()
        conn.close()
        return reportdetails
    
    def get_reports_by_user(self, user_id):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        cur.execute("SELECT * FROM reports WHERE user_id = ?", (user_id,))
        report_list = cur.fetchall()
        conn.close()
        return report_list

    def delete_report(self, id):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        cur.execute("delete from reports where id=?", (id))
        conn.commit()
        conn.close()
    def delete_user(self, id):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        cur.execute("delete from users where id=?", (id))
        conn.commit()
        conn.close()
        
    def update_report(self, report_id, pet_name=None, pet_type=None, location=None, description=None, photo_path=None):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
    
        update_fields = []
        values = []
    
        if pet_name:
            update_fields.append("pet_name = ?")
            values.append(pet_name)
        if pet_type:
            update_fields.append("pet_type = ?")
            values.append(pet_type)
        if location:
            update_fields.append("location = ?")
            values.append(location)
        if description:
            update_fields.append("description = ?")
            values.append(description)
        if photo_path:
            update_fields.append("photo_path = ?")
            values.append(photo_path)

        values.append(report_id)
    
        cur.execute(f"UPDATE reports SET {', '.join(update_fields)} WHERE id = ?", tuple(values))
    
        conn.commit()
        conn.close()
