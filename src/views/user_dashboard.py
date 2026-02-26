import customtkinter as ctk
from PIL import Image
from .seat_selection import SeatSelectionView

class UserDashboard(ctk.CTkFrame):
    def __init__(self, master, booking_service, user):
        super().__init__(master)
        self.booking_service = booking_service
        self.user = user
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.setup_ui()

    def setup_ui(self):
        # Sidebar for Filtering
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="Cinema Pro", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(pady=20)
        
        self.search_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Search movies...")
        self.search_entry.pack(pady=10, padx=20)
        
        self.search_btn = ctk.CTkButton(self.sidebar, text="Search", command=self.handle_search)
        self.search_btn.pack(pady=10, padx=20)
        
        self.filter_label = ctk.CTkLabel(self.sidebar, text="Filters", font=ctk.CTkFont(size=14, weight="bold"))
        self.filter_label.pack(pady=(20, 10))
        
        self.genre_filter = ctk.CTkOptionMenu(self.sidebar, values=["All Genres", "Action", "Drama", "Sci-Fi", "Comedy"])
        self.genre_filter.pack(pady=10, padx=20)

        ctk.CTkButton(self.sidebar, text="Logout", fg_color="gray30", command=self.master.logout).pack(side="bottom", pady=20)

        # Main Content Area
        self.content_area = ctk.CTkScrollableFrame(self)
        self.content_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.load_movies()

    def load_movies(self, search_term=None):
        # Clear previous movies
        for widget in self.content_area.winfo_children():
            widget.destroy()

        if search_term:
            movies = self.booking_service.movie_model.search_movies(search_term)
        else:
            movies = self.booking_service.get_available_movies()
        
        for i, movie in enumerate(movies):
            self.create_movie_card(movie, i)

    def create_movie_card(self, movie, index):
        card = ctk.CTkFrame(self.content_area, corner_radius=10)
        card.pack(fill="x", pady=10, padx=10)
        
        # Details
        details_frame = ctk.CTkFrame(card, fg_color="transparent")
        details_frame.pack(side="left", padx=20, pady=10, fill="both", expand=True)
        
        title = ctk.CTkLabel(details_frame, text=movie['title'], font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(anchor="w")
        
        info = ctk.CTkLabel(details_frame, text=f"Rating: {movie['rating']} | {movie['duration_minutes']} mins | {movie['director']}", font=ctk.CTkFont(size=12))
        info.pack(anchor="w")
        
        desc = ctk.CTkLabel(details_frame, text=f"{movie['description'][:150]}..." if movie['description'] else "No description available", font=ctk.CTkFont(size=11), wraplength=400, justify="left")
        desc.pack(anchor="w", pady=5)
        
        # Action
        btn = ctk.CTkButton(card, text="Book Now", command=lambda m=movie: self.on_book_click(m))
        btn.pack(side="right", padx=20)

    def handle_search(self):
        term = self.search_entry.get()
        self.load_movies(term)

    def on_book_click(self, movie):
        shows = self.booking_service.get_shows_for_movie(movie['id'])
        if not shows:
            print("No upcoming shows for this movie.")
            return
        
        # For simplicity, pick the first show. In a full app, show a list.
        show = shows[0]
        
        # Open Seat Selection Window
        self.seat_selection = SeatSelectionView(self, movie, show, self.booking_service, self.on_booking_complete)

    def on_booking_complete(self, ticket_path):
        from tkinter import messagebox
        messagebox.showinfo("Success", f"Ticket booked! \nGenerated: {ticket_path}")
