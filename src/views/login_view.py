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
        # Background Decoration (Optional: can add image here)
        self.bg_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bg_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Header with subtle glow effect
        self.label = ctk.CTkLabel(
            self.bg_frame, 
            text="CINEMA PRO", 
            font=ctk.CTkFont(family="Inter", size=48, weight="bold"),
            text_color="#c0392b"
        )
        self.label.pack(pady=(0, 40))

        # DB Settings Button (Top Right)
        self.settings_btn = ctk.CTkButton(
            self, text="⚙ Settings", width=100, 
            fg_color="transparent", border_width=1, 
            command=self.open_settings
        )
        self.settings_btn.place(relx=0.98, rely=0.02, anchor="ne")

        # Main Card
        self.card = ctk.CTkFrame(self.bg_frame, width=450, height=500, corner_radius=15, border_width=1)
        self.card.pack(padx=20, pady=10)
        self.card.pack_propagate(False)

        # Tabview for Login/Register
        self.tabview = ctk.CTkTabview(self.card, width=400)
        self.tabview.pack(pady=30, padx=30, expand=True, fill="both")
        self.tabview.add("LOGIN")
        self.tabview.add("SIGN UP")

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
        
        # 1. Database Check (Authentication)
        try:
            success, result = self.auth_service.login(username, password)
        except Exception as e:
            self.login_status.configure(text=f"Connection Error: {str(e)[:40]}")
            print("ERROR:", e)
            return

        if not success:
            self.login_status.configure(text=result)
            return
            
        # 2. Page Transition (Routing)
        try:
            self.on_login_success(result)
        except Exception as e:
            print("ERROR during dashboard building:", e)
            import traceback
            traceback.print_exc()

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
        except Exception as e:
            self.signup_status.configure(text=f"Error: {str(e)[:50]}...", text_color="red")
            print(f"Signup exception: {e}")
    def open_settings(self):
        SettingsView(self, self.on_settings_saved)

    def on_settings_saved(self):
        # Refresh services with new config
        self.auth_service.__init__() 
        self.login_status.configure(text="Settings saved! Try logging in.", text_color="green")
