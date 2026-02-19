import mysql.connector
import tkinter as tk
from tkinter import simpledialog, messagebox
import os

def setup_database():
    """
    Initializes the database by running schema.sql and sample_data.sql.
    """
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

    # 2. Execute SQL Files
    cursor = conn.cursor()
    
    # Define files to run
    base_dir = os.path.dirname(os.path.abspath(__file__))
    files = ["schema.sql", "sample_data.sql"]
    
    for filename in files:
        file_path = os.path.join(base_dir, filename)
        if not os.path.exists(file_path):
            print(f"Skipping {filename}: File not found.")
            continue

        try:
            with open(file_path, 'r') as f:
                sql_script = f.read()
            
            print(f"Executing {filename}...")
            # Execute with multi=True
            for result in cursor.execute(sql_script, multi=True):
                if result.with_rows:
                    result.fetchall()
            conn.commit()
            print(f"Successfully executed {filename}.")
            
        except mysql.connector.Error as e:
            messagebox.showerror("SQL Error", f"Error executing {filename}:\n{e}")
            print(f"SQL Error in {filename}: {e}")
            
    messagebox.showinfo("Success", "Database verification and setup complete!")

    if conn and conn.is_connected():
        cursor.close()
        conn.close()

if __name__ == "__main__":
    setup_database()
