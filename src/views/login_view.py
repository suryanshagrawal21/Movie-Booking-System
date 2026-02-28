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
        # Background Frame (Could be replaced with a poster collage and dark overlay)
        self.bg_frame = ctk.CTkFrame(self, fg_color="#0a0a0a")
        self.bg_frame.pack(fill="both", expand=True)

        # Centered Container
        self.center_container = ctk.CTkFrame(self.bg_frame, fg_color="transparent")
        self.center_container.place(relx=0.5, rely=0.5, anchor="center")

        # Animated-style Header
        self.header_frame = ctk.CTkFrame(self.center_container, fg_color="transparent")
        self.header_frame.pack(pady=(0, 30))
        
        self.logo = ctk.CTkLabel(self.header_frame, text="CINEMA", font=ctk.CTkFont(family="Inter", size=48, weight="bold"), text_color="#f1f1f1")
        self.logo.pack(side="left")
        self.pro = ctk.CTkLabel(self.header_frame, text="PRO", font=ctk.CTkFont(family="Inter", size=48, weight="bold"), text_color="#e50914") # Netflix Red
        self.pro.pack(side="left", padx=(5, 0))
        
        self.tagline = ctk.CTkLabel(self.center_container, text="Your Premium Movie Experience", font=ctk.CTkFont(size=14), text_color="#888888")
        self.tagline.pack(pady=(0, 20))

        # DB Settings Button (Top Right)
        self.settings_btn = ctk.CTkButton(
            self.bg_frame, text="⚙ Settings", width=100, 
            fg_color="transparent", border_width=1, border_color="#333333",
            hover_color="#1a1a1a", command=self.open_settings
        )
        self.settings_btn.place(relx=0.97, rely=0.03, anchor="ne")

        # Main Glassmorphism-style Card
        self.card = ctk.CTkFrame(self.center_container, width=400, height=500, corner_radius=15, fg_color="#111111", border_width=1, border_color="#2f2f2f")
        self.card.pack(padx=20, pady=10)
        self.card.pack_propagate(False)

        # Tabview for Login/Register
        self.tabview = ctk.CTkTabview(self.card, width=360, segmented_button_selected_color="#e50914", segmented_button_selected_hover_color="#b80710")
        self.tabview.pack(pady=20, padx=20, expand=True, fill="both")
        self.tabview.add("LOGIN")
        self.tabview.add("SIGN UP")

        self.setup_login_tab()
        self.setup_signup_tab()

    def setup_login_tab(self):
        tab = self.tabview.tab("LOGIN")
        
        self.login_username = ctk.CTkEntry(tab, placeholder_text="Email or Username", width=300, height=45, corner_radius=8, border_width=0, fg_color="#222222")
        self.login_username.pack(pady=(30, 15))
        
        self.login_password = ctk.CTkEntry(tab, placeholder_text="Password", show="•", width=300, height=45, corner_radius=8, border_width=0, fg_color="#222222")
        self.login_password.pack(pady=15)
        
        self.login_button = ctk.CTkButton(tab, text="Sign In", command=self.handle_login, width=300, height=45, corner_radius=8, font=ctk.CTkFont(weight="bold"), fg_color="#e50914", hover_color="#b80710")
        self.login_button.pack(pady=25)

        self.login_status = ctk.CTkLabel(tab, text="", text_color="#ff4d4d")
        self.login_status.pack()

    def setup_signup_tab(self):
        tab = self.tabview.tab("SIGN UP")
        
        self.signup_username = ctk.CTkEntry(tab, placeholder_text="Username", width=300, height=40, corner_radius=8, border_width=0, fg_color="#222222")
        self.signup_username.pack(pady=(20, 10))
        
        self.signup_email = ctk.CTkEntry(tab, placeholder_text="Email Address", width=300, height=40, corner_radius=8, border_width=0, fg_color="#222222")
        self.signup_email.pack(pady=10)
        
        self.signup_password = ctk.CTkEntry(tab, placeholder_text="Password (min 6 chars)", show="•", width=300, height=40, corner_radius=8, border_width=0, fg_color="#222222")
        self.signup_password.pack(pady=10)
        
        self.signup_button = ctk.CTkButton(tab, text="Create Account", command=self.handle_signup, width=300, height=45, corner_radius=8, font=ctk.CTkFont(weight="bold"), fg_color="#e50914", hover_color="#b80710")
        self.signup_button.pack(pady=20)

        self.signup_status = ctk.CTkLabel(tab, text="", text_color="#ff4d4d")
        self.signup_status.pack()

    def handle_login(self):
        username = self.login_username.get()
        password = self.login_password.get()
        
        # 1. Database Check (Authentication)
        try:
            self.login_button.configure(text="Authenticating...", state="disabled")
            self.update_idletasks()
            success, result = self.auth_service.login(username, password)
        except Exception as e:
            self.login_status.configure(text="Database Error. Try again later.")
            print("Login Error Details:", e)
            self.login_button.configure(text="Sign In", state="normal")
            return

        self.login_button.configure(text="Sign In", state="normal")

        if not success:
            if "Connection Error" in result:
                self.login_status.configure(text="DB Connection Error! Check Settings ⚙")
            else:
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
                if "Connection Error" in message or "Registration failed" in message:
                    self.signup_status.configure(text="DB Error! Check Settings ⚙", text_color="red")
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
