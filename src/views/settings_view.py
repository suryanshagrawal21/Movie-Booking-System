import customtkinter as ctk
from ..utils.config_manager import ConfigManager
from ..models.base_model import BaseModel
from tkinter import messagebox

class SettingsView(ctk.CTkToplevel):
    def __init__(self, master, on_save_callback):
        super().__init__(master)
        self.title("Database Settings")
        self.geometry("400x450")
        self.on_save_callback = on_save_callback
        
        self.setup_ui()

    def setup_ui(self):
        config = ConfigManager.load_config()
        
        ctk.CTkLabel(self, text="MySQL Connection Settings", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        self.host = self.create_input("Host:", config["db_host"])
        self.user = self.create_input("User:", config["db_user"])
        self.password = self.create_input("Password:", config["db_password"], show="*")
        self.database = self.create_input("Database:", config["db_name"])
        
        self.test_btn = ctk.CTkButton(self, text="Test Connection", fg_color="gray", command=self.test_connection)
        self.test_btn.pack(pady=10)
        
        self.save_btn = ctk.CTkButton(self, text="Save & Connect", command=self.save_settings)
        self.save_btn.pack(pady=20)

    def create_input(self, label, value, **kwargs):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="x", padx=40, pady=5)
        ctk.CTkLabel(frame, text=label).pack(side="left")
        entry = ctk.CTkEntry(frame, **kwargs)
        entry.insert(0, value)
        entry.pack(side="right", fill="x", expand=True, padx=(10, 0))
        return entry

    def test_connection(self):
        db = BaseModel()
        if db.test_connection(self.host.get(), self.user.get(), self.password.get()):
            messagebox.showinfo("Success", "Connection successful!")
        else:
            messagebox.showerror("Error", "Could not connect to MySQL.")

    def save_settings(self):
        ConfigManager.update_db_credentials(
            self.host.get(), self.user.get(), self.password.get(), self.database.get()
        )
        self.on_save_callback()
        self.destroy()
