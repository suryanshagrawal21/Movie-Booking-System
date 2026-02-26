import customtkinter as ctk
from .login_view import LoginView
from .user_dashboard import UserDashboard
from .admin_dashboard import AdminDashboard
from ..controllers.auth_service import AuthService
from ..controllers.booking_service import BookingService

class MovieApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Cinema Pro - Movie Booking System")
        self.geometry("1100x700")
        
        # Set Appearance
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.auth_service = AuthService()
        self.booking_service = BookingService()
        
        # Main Container
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)
        
        self.show_login()

    def show_login(self):
        self.clear_container()
        self.login_frame = LoginView(self.container, self.auth_service, self.on_login_success)
        self.login_frame.pack(fill="both", expand=True)

    def on_login_success(self, user):
        print(f"Logged in as: {user['username']} ({user['role']})")
        if user['role'] == 'admin':
            self.show_admin_dashboard()
        else:
            self.show_user_dashboard()

    def show_user_dashboard(self):
        self.clear_container()
        self.dashboard = UserDashboard(self.container, self.booking_service, self.auth_service.current_user)
        self.dashboard.pack(fill="both", expand=True)

    def show_admin_dashboard(self):
        self.clear_container()
        self.dashboard = AdminDashboard(self.container, self.booking_service, self.auth_service.current_user)
        self.dashboard.pack(fill="both", expand=True)

    def logout(self):
        self.auth_service.logout()
        self.show_login()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = MovieApp()
    app.mainloop()
