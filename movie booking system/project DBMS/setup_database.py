import mysql.connector
import tkinter as tk
from tkinter import simpledialog, messagebox
import os

def setup_database():
    root = tk.Tk()
    root.withdraw()  # Hide main window

    # 1. Acquire Password
    password = "Divya.21" # Default
    conn = None
    
    # Try default first
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password=password)
    except mysql.connector.Error:
        pass
        
    if not conn or not conn.is_connected():
        password = simpledialog.askstring("Database Setup", "MySQL Connection Failed.\nEnter Root Password:", show='*')
        if password is None:
            print("Setup cancelled.")
            return

        try:
            conn = mysql.connector.connect(host="localhost", user="root", password=password)
        except mysql.connector.Error as e:
            messagebox.showerror("Connection Error", f"Could not connect to MySQL:\n{e}")
            return

    # 2. Execute SQL File
    cursor = conn.cursor()
    sql_file_path = "moviebooking.sql"
    
    if not os.path.exists(sql_file_path):
        messagebox.showerror("Error", f"File not found: {sql_file_path}")
        return

    try:
        with open(sql_file_path, 'r') as f:
            sql_script = f.read()
        
        # Execute with multi=True to handle multiple statements
        # Note: mysql-connector might have issues with some delimiters, but standard ; should work
        for result in cursor.execute(sql_script, multi=True):
            if result.with_rows:
                result.fetchall() # Consume results
                
        conn.commit()
        messagebox.showinfo("Success", "Database and Tables created successfully!")
        print("Database setup complete.")
        
    except mysql.connector.Error as e:
        messagebox.showerror("SQL Error", f"Error executing script:\n{e}")
        print(f"SQL Error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    setup_database()
