import customtkinter as ctk
from PIL import Image
from .seat_selection import SeatSelectionView
from tkinter import messagebox

class UserDashboard(ctk.CTkFrame):
    def __init__(self, master, booking_service, user):
        super().__init__(master)
        self.booking_service = booking_service
        self.user = user
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.setup_ui()

    def setup_ui(self):
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#1a1a1a", border_width=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="🎬 CINEMA PRO", font=ctk.CTkFont(size=22, weight="bold"), text_color="#c0392b")
        self.logo_label.pack(pady=40, padx=20)
        
        self.nav_movies_btn = ctk.CTkButton(
            self.sidebar, text="  🎥  Movies", 
            anchor="w", fg_color="transparent", 
            height=45, font=ctk.CTkFont(size=14),
            command=self.show_movies
        )
        self.nav_movies_btn.pack(pady=5, padx=20, fill="x")
        
        self.nav_history_btn = ctk.CTkButton(
            self.sidebar, text="  🎟️  My Bookings", 
            anchor="w", fg_color="transparent", 
            height=45, font=ctk.CTkFont(size=14),
            command=self.show_history
        )
        self.nav_history_btn.pack(pady=5, padx=20, fill="x")

        # Logout button
        ctk.CTkButton(
            self.sidebar, text="Logout", 
            fg_color="transparent", border_width=1, 
            border_color="#c0392b", hover_color="#c0392b",
            command=self.master.master.logout
        ) .pack(side="bottom", pady=30, padx=30, fill="x")

        # Main Content Area
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)
        
        self.show_movies()

    def clear_main_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def show_movies(self):
        self.clear_main_container()
        
        header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 30))
        
        ctk.CTkLabel(header_frame, text="Explore Movies", font=ctk.CTkFont(family="Inter", size=32, weight="bold")).pack(side="left")
        
        search_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        search_frame.pack(side="right")
        
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search movies...", width=250, height=40)
        self.search_entry.pack(side="left", padx=10)
        
        ctk.CTkButton(search_frame, text="Search", width=100, height=40, command=self.handle_search).pack(side="left")

        self.content_area = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        self.content_area.pack(fill="both", expand=True)
        
        self.load_movies()

    def load_movies(self, search_term=None):
        for widget in self.content_area.winfo_children():
            widget.destroy()

        if search_term:
            movies = self.booking_service.movie_model.search_movies(search_term)
        else:
            movies = self.booking_service.get_available_movies()
        
        if not movies:
            ctk.CTkLabel(self.content_area, text="No movies found.", font=ctk.CTkFont(size=16)).pack(pady=40)
            return

        for movie in movies:
            self.create_movie_card(movie)

    def create_movie_card(self, movie):
        card = ctk.CTkFrame(self.content_area, corner_radius=15, border_width=1, border_color="#2f2f2f")
        card.pack(fill="x", pady=12, padx=10)
        
        # Details Inner Frame
        details_frame = ctk.CTkFrame(card, fg_color="transparent")
        details_frame.pack(side="left", padx=25, pady=20, fill="both", expand=True)
        
        ctk.CTkLabel(details_frame, text=movie['title'].upper(), font=ctk.CTkFont(size=20, weight="bold"), text_color="#f1f1f1").pack(anchor="w")
        
        meta_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
        meta_frame.pack(anchor="w", pady=(5, 0))
        
        ctk.CTkLabel(meta_frame, text=f"⏱ {movie['duration_minutes']} MINS", font=ctk.CTkFont(size=12, weight="bold"), text_color="#888888").pack(side="left")
        ctk.CTkLabel(meta_frame, text=" | ", text_color="#444444").pack(side="left", padx=5)
        ctk.CTkLabel(meta_frame, text=f"⭐ {movie['rating']}", font=ctk.CTkFont(size=12, weight="bold"), text_color="#f1c40f").pack(side="left")
        
        ctk.CTkLabel(details_frame, text=movie['director'], font=ctk.CTkFont(size=13), text_color="#666666").pack(anchor="w", pady=(5, 0))

        ctk.CTkButton(
            card, text="BOOK TICKETS", 
            width=150, height=45, corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=lambda m=movie: self.on_book_click(m)
        ).pack(side="right", padx=25)

    def handle_search(self):
        self.load_movies(self.search_entry.get())

    def on_book_click(self, movie):
        shows = self.booking_service.get_shows_for_movie(movie['id'])
        if not shows:
            messagebox.showinfo("Wait", "No upcoming shows for this movie yet.")
            return
        
        # Show selection modal
        show_window = ctk.CTkToplevel(self)
        show_window.title(f"Select Show - {movie['title']}")
        show_window.geometry("400x500")
        
        ctk.CTkLabel(show_window, text="Available Shows", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)
        
        for show in shows:
            btn = ctk.CTkButton(
                show_window, 
                text=f"{show['show_time']} \n{show['theater_name']} (${show['base_price']})",
                command=lambda s=show: self.open_seat_selection(movie, s, show_window)
            )
            btn.pack(pady=10, padx=20, fill="x")

    def open_seat_selection(self, movie, show, window):
        window.destroy()
        SeatSelectionView(self, movie, show, self.booking_service, self.on_booking_complete)

    def show_history(self):
        self.clear_main_container()
        ctk.CTkLabel(self.main_container, text="My Booking History", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(0, 20))
        
        history_frame = ctk.CTkScrollableFrame(self.main_container)
        history_frame.pack(fill="both", expand=True)
        
        bookings = self.booking_service.get_user_history(self.user['id'])
        
        if not bookings:
            ctk.CTkLabel(history_frame, text="You have no bookings yet.").pack(pady=20)
            return

        for b in bookings:
            f = ctk.CTkFrame(history_frame)
            f.pack(fill="x", pady=5, padx=5)
            
            ctk.CTkLabel(f, text=b['movie_title'], font=ctk.CTkFont(weight="bold")).pack(side="left", padx=10)
            ctk.CTkLabel(f, text=f"Time: {b['show_time']} | Price: ${b['total_price']}").pack(side="left", padx=20)
            
            # Button to view ticket
            ticket_path = f"tickets/ticket_{b['id']}.pdf"
            if os.path.exists(ticket_path):
                ctk.CTkButton(f, text="📄 View Ticket", width=100, command=lambda p=ticket_path: os.startfile(p)).pack(side="right", padx=10, pady=5)

    def on_booking_complete(self, ticket_path):
        messagebox.showinfo("Success", f"Ticket booked successfully!\nTicket saved at: {ticket_path}")
        if os.path.exists(ticket_path):
            os.startfile(ticket_path)
        self.show_history()
