import customtkinter as ctk

class AdminDashboard(ctk.CTkFrame):
    def __init__(self, master, booking_service, user):
        super().__init__(master)
        self.booking_service = booking_service
        self.user = user
        self.setup_ui()

    def setup_ui(self):
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.tabview.add("Manage Movies")
        self.tabview.add("Manage Shows")
        self.tabview.add("View Bookings")
        
        self.setup_movie_management()
        self.setup_show_management()

    def setup_movie_management(self):
        tab = self.tabview.tab("Manage Movies")
        
        # Left: Form
        form_frame = ctk.CTkFrame(tab, width=300)
        form_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        ctk.CTkLabel(form_frame, text="Add New Movie", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        self.movie_title = ctk.CTkEntry(form_frame, placeholder_text="Title")
        self.movie_title.pack(pady=5, padx=10, fill="x")
        
        self.movie_desc = ctk.CTkTextbox(form_frame, height=100)
        self.movie_desc.pack(pady=5, padx=10, fill="x")
        
        # ... more fields ...
        
        ctk.CTkButton(form_frame, text="Add Movie", command=self.add_movie).pack(pady=20)

        # Right: List
        self.movie_list = ctk.CTkScrollableFrame(tab)
        self.movie_list.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        self.refresh_movie_list()

    def refresh_movie_list(self):
        for widget in self.movie_list.winfo_children():
            widget.destroy()
        
        movies = self.booking_service.get_available_movies()
        for movie in movies:
            f = ctk.CTkFrame(self.movie_list)
            f.pack(fill="x", pady=5)
            ctk.CTkLabel(f, text=movie['title']).pack(side="left", padx=10)
            ctk.CTkButton(f, text="Delete", fg_color="red", width=60, command=lambda m=movie: self.delete_movie(m)).pack(side="right", padx=10)

    def setup_show_management(self):
        tab = self.tabview.tab("Manage Shows")
        ctk.CTkLabel(tab, text="Show management coming soon...").pack(pady=20)

    def add_movie(self):
        title = self.movie_title.get()
        desc = self.movie_desc.get("1.0", "end")
        # Validation and call model
        print(f"Adding movie: {title}")

    def delete_movie(self, movie):
        if self.booking_service.movie_model.delete_movie(movie['id']):
            self.refresh_movie_list()
