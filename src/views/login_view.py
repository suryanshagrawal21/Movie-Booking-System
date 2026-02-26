import customtkinter as ctk
from PIL import Image
import os
from .settings_view import SettingsView

class LoginView(ctk.CTkFrame):
    def __init__(self, master, auth_service, on_login_success):
        super().__init__(master)
        self.auth_service = auth_service
        self.on_login_success = on_login_success
        
        self.grid_columnconfigure(0, weight=1)
        self.setup_ui()

    def setup_ui(self):
        # Header
        self.label = ctk.CTkLabel(self, text="Movie Booking System", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=(40, 10))

        # DB Settings Button (Top Right)
        self.settings_btn = ctk.CTkButton(self, text="⚙ DB Settings", width=80, fg_color="gray30", command=self.open_settings)
        self.settings_btn.place(relx=0.95, rely=0.05, anchor="ne")

        # Tabview for Login/Register
        self.tabview = ctk.CTkTabview(self, width=400)
        self.tabview.pack(pady=10, padx=40, expand=True, fill="both")
        self.tabview.add("Login")
        self.tabview.add("Sign Up")

        self.setup_login_tab()
        self.setup_signup_tab()

    def setup_login_tab(self):
        tab = self.tabview.tab("Login")
        
        self.login_username = ctk.CTkEntry(tab, placeholder_text="Username", width=300)
        self.login_username.pack(pady=15)
        
        self.login_password = ctk.CTkEntry(tab, placeholder_text="Password", show="*", width=300)
        self.login_password.pack(pady=15)
        
        self.login_button = ctk.CTkButton(tab, text="Login", command=self.handle_login, width=300)
        self.login_button.pack(pady=20)

        self.login_status = ctk.CTkLabel(tab, text="", text_color="red")
        self.login_status.pack()

    def setup_signup_tab(self):
        tab = self.tabview.tab("Sign Up")
        
        self.signup_username = ctk.CTkEntry(tab, placeholder_text="Username", width=300)
        self.signup_username.pack(pady=10)
        
        self.signup_email = ctk.CTkEntry(tab, placeholder_text="Email", width=300)
        self.signup_email.pack(pady=10)
        
        self.signup_password = ctk.CTkEntry(tab, placeholder_text="Password", show="*", width=300)
        self.signup_password.pack(pady=10)
        
        self.signup_button = ctk.CTkButton(tab, text="Register", command=self.handle_signup, width=300)
        self.signup_button.pack(pady=20)

        self.signup_status = ctk.CTkLabel(tab, text="", text_color="red")
        self.signup_status.pack()

    def handle_login(self):
        username = self.login_username.get()
        password = self.login_password.get()
        
        try:
            success, result = self.auth_service.login(username, password)
            if success:
                self.on_login_success(result)
            else:
                self.login_status.configure(text=result)
        except Exception as e:
            self.login_status.configure(text="Connection Error. Check DB Settings.")
            print(f"Login error: {e}")

    def handle_signup(self):
        username = self.signup_username.get()
        email = self.signup_email.get()
        password = self.signup_password.get()
        
        if not username or not email or not password:
            self.signup_status.configure(text="Please fill all fields.")
            return

        try:
            success, message = self.auth_service.register(username, email, password)
            if success:
                self.signup_status.configure(text="Account created! Please login.", text_color="green")
            else:
                self.signup_status.configure(text=message, text_color="red")
        except Exception:
            self.signup_status.configure(text="Connection Error. Check DB Settings.")

    def open_settings(self):
        SettingsView(self, self.on_settings_saved)

    def on_settings_saved(self):
        # Refresh services with new config
        self.auth_service.__init__() 
        self.login_status.configure(text="Settings saved! Try logging in.", text_color="green")
