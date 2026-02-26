import customtkinter as ctk
from tkinter import messagebox

class AdminDashboard(ctk.CTkFrame):
    def __init__(self, master, booking_service, user):
        super().__init__(master)
        self.booking_service = booking_service
        self.user = user
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.setup_ui()

    def setup_ui(self):
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.tabview.add("Manage Movies")
        self.tabview.add("Manage Shows")
        self.tabview.add("View Bookings")
        
        self.setup_movie_management()
        self.setup_show_management()
        self.setup_booking_view()

    def setup_movie_management(self):
        tab = self.tabview.tab("Manage Movies")
        
        # Left: Add Movie Form
        form_frame = ctk.CTkFrame(tab, width=350)
        form_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        ctk.CTkLabel(form_frame, text="Add New Movie", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        self.movie_title = ctk.CTkEntry(form_frame, placeholder_text="Title")
        self.movie_title.pack(pady=5, padx=10, fill="x")
        
        self.movie_desc = ctk.CTkTextbox(form_frame, height=80)
        self.movie_desc.pack(pady=5, padx=10, fill="x")
        self.movie_desc.insert("1.0", "Description...")
        
        self.movie_director = ctk.CTkEntry(form_frame, placeholder_text="Director")
        self.movie_director.pack(pady=5, padx=10, fill="x")
        
        self.movie_cast = ctk.CTkEntry(form_frame, placeholder_text="Cast (comma separated)")
        self.movie_cast.pack(pady=5, padx=10, fill="x")
        
        self.movie_duration = ctk.CTkEntry(form_frame, placeholder_text="Duration (mins)")
        self.movie_duration.pack(pady=5, padx=10, fill="x")
        
        self.movie_rating = ctk.CTkEntry(form_frame, placeholder_text="Rating (0.0 - 10.0)")
        self.movie_rating.pack(pady=5, padx=10, fill="x")
        
        self.movie_date = ctk.CTkEntry(form_frame, placeholder_text="Release Date (YYYY-MM-DD)")
        self.movie_date.pack(pady=5, padx=10, fill="x")

        ctk.CTkButton(form_frame, text="Save Movie", command=self.add_movie, fg_color="#27ae60", hover_color="#2ecc71").pack(pady=20, padx=10, fill="x")

        # Right: Movie List
        list_frame = ctk.CTkFrame(tab)
        list_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(list_frame, text="Current Movies", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        self.movie_list_scroll = ctk.CTkScrollableFrame(list_frame)
        self.movie_list_scroll.pack(fill="both", expand=True)
        
        self.refresh_movie_list()

    def refresh_movie_list(self):
        for widget in self.movie_list_scroll.winfo_children():
            widget.destroy()
        
        movies = self.booking_service.get_available_movies()
        for movie in movies:
            f = ctk.CTkFrame(self.movie_list_scroll)
            f.pack(fill="x", pady=5, padx=5)
            
            ctk.CTkLabel(f, text=movie['title'], font=ctk.CTkFont(weight="bold")).pack(side="left", padx=10)
            ctk.CTkLabel(f, text=f"ID: {movie['id']}", font=ctk.CTkFont(size=10)).pack(side="left", padx=10)
            
            ctk.CTkButton(f, text="Delete", fg_color="#c0392b", hover_color="#e74c3c", width=60, command=lambda m=movie: self.delete_movie(m)).pack(side="right", padx=10, pady=5)

    def setup_show_management(self):
        tab = self.tabview.tab("Manage Shows")
        
        form_frame = ctk.CTkFrame(tab, width=350)
        form_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        ctk.CTkLabel(form_frame, text="Schedule New Show", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        self.show_movie_id = ctk.CTkEntry(form_frame, placeholder_text="Movie ID")
        self.show_movie_id.pack(pady=5, padx=10, fill="x")
        
        self.show_theater_id = ctk.CTkEntry(form_frame, placeholder_text="Theater ID")
        self.show_theater_id.pack(pady=5, padx=10, fill="x")
        
        self.show_time = ctk.CTkEntry(form_frame, placeholder_text="Show Time (YYYY-MM-DD HH:MM:SS)")
        self.show_time.pack(pady=5, padx=10, fill="x")
        
        self.show_price = ctk.CTkEntry(form_frame, placeholder_text="Base Price")
        self.show_price.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(form_frame, text="Schedule Show", command=self.add_show, fg_color="#27ae60").pack(pady=20, padx=10, fill="x")

    def setup_booking_view(self):
        tab = self.tabview.tab("View Bookings")
        ctk.CTkLabel(tab, text="Booking reports and analytics coming soon...").pack(pady=20)

    def add_movie(self):
        try:
            data = {
                "title": self.movie_title.get(),
                "description": self.movie_desc.get("1.0", "end-1c"),
                "director": self.movie_director.get(),
                "cast": self.movie_cast.get(),
                "duration_minutes": int(self.movie_duration.get()),
                "rating": float(self.movie_rating.get()),
                "release_date": self.movie_date.get()
            }
            
            if self.booking_service.movie_model.add_movie(**data):
                messagebox.showinfo("Success", "Movie added successfully!")
                self.refresh_movie_list()
            else:
                messagebox.showerror("Error", "Failed to add movie.")
        except Exception as e:
            messagebox.showerror("Validation Error", str(e))

    def add_show(self):
        try:
            m_id = int(self.show_movie_id.get())
            t_id = int(self.show_theater_id.get())
            time = self.show_time.get()
            price = float(self.show_price.get())
            
            if self.booking_service.show_model.add_show(m_id, t_id, time, price):
                messagebox.showinfo("Success", "Show scheduled successfully!")
            else:
                messagebox.showerror("Error", "Failed to schedule show.")
        except Exception as e:
            messagebox.showerror("Validation Error", str(e))

    def delete_movie(self, movie):
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete '{movie['title']}'?"):
            if self.booking_service.movie_model.delete_movie(movie['id']):
                self.refresh_movie_list()
