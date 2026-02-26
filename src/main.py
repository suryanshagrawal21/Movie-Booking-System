import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from database import DatabaseManager

class MovieBookingApp(tk.Tk):
    """
    Main Application Class for the Movie Booking System.
    Inherits from tk.Tk.
    """
    def __init__(self):
        super().__init__()
        self.title("Movie Booking System")
        self.geometry("1100x750")
        self.configure(bg="#2c3e50") # Dark Blue-Grey

        # Style Configuration
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.configure_styles()

        # Database Connection
        self.db = DatabaseManager(password="Divya.21") # Try default password
        if not self.db.connect():
             # If default fails, ask user
             pwd = simpledialog.askstring("Database Password", "MySQL Connection Failed.\nEnter MySQL Root Password:", show='*')
             if pwd:
                 self.db = DatabaseManager(password=pwd)
                 if not self.db.connect():
                     messagebox.showerror("Error", "Could not connect to database. Please check your password and ensure MySQL is running.")
                     self.destroy()
                     return
             else:
                 self.destroy()
                 return

        # UI Layout
        self.create_widgets()

    def configure_styles(self):
        """Configures the custom Tkinter styles."""
        bg_color = "#2c3e50"
        fg_color = "white"
        accent_color = "#e67e22" # Orange
        
        self.style.configure("TFrame", background=bg_color)
        self.style.configure("TLabel", background=bg_color, foreground=fg_color, font=("Segoe UI", 11))
        self.style.configure("TButton", background=accent_color, foreground="white", font=("Segoe UI", 10, "bold"), padding=6)
        self.style.map("TButton", background=[('active', '#d35400')]) 
        
        self.style.configure("Header.TLabel", font=("Segoe UI", 24, "bold"), foreground=accent_color)
        
        self.style.configure("Treeview", 
                             background="white", 
                             foreground="black", 
                             fieldbackground="white",
                             font=("Segoe UI", 10),
                             rowheight=25)
        self.style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
        
        self.style.configure("TLabelframe", background=bg_color, foreground=fg_color)
        self.style.configure("TLabelframe.Label", background=bg_color, foreground=accent_color, font=("Segoe UI", 12, "bold"))

    def create_widgets(self):
        """Creates and packs the GUI widgets."""
        # Main Container
        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        header = ttk.Label(main_container, text="🎬 Movie Booking System", style="Header.TLabel")
        header.pack(side=tk.TOP, fill=tk.X, pady=(0, 20))

        # Content Split (Left: Form, Right: List)
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # --- Left Panel: Management Form ---
        left_panel = ttk.LabelFrame(content_frame, text="Manage Movies", padding=15)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))

        # Form Entries
        self.vars = {
            "movie_id": tk.StringVar(),
            "name": tk.StringVar(),
            "release_date": tk.StringVar(),
            "director": tk.StringVar(),
            "cast": tk.StringVar(),
            "budget": tk.StringVar(),
            "duration": tk.StringVar(),
            "rating": tk.StringVar()
        }

        # Label Text and Variable mapping
        labels = [
            ("Movie ID", "movie_id"), ("Movie Name", "name"), ("Release Date (YYYY-MM-DD)", "release_date"),
            ("Director", "director"), ("Cast", "cast"), ("Budget", "budget"),
            ("Duration (Hrs)", "duration"), ("Rating (0-10)", "rating")
        ]

        for i, (text, var_name) in enumerate(labels):
            lbl = ttk.Label(left_panel, text=text)
            lbl.grid(row=i, column=0, sticky="w", pady=5)
            
            entry = ttk.Entry(left_panel, textvariable=self.vars[var_name], width=30)
            entry.grid(row=i, column=1, sticky="ew", pady=5, padx=(10, 0))

        # Action Buttons
        btn_frame = ttk.Frame(left_panel)
        btn_frame.grid(row=len(labels), column=0, columnspan=2, pady=20)

        ttk.Button(btn_frame, text="Add", command=self.add_movie).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(btn_frame, text="Update", command=self.update_movie).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_movie).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_form).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Separator(left_panel, orient='horizontal').grid(row=len(labels)+1, column=0, columnspan=2, sticky="ew", pady=10)
        
        # Booking Section
        ttk.Label(left_panel, text="Booking Actions", style="TLabelframe.Label").grid(row=len(labels)+2, column=0, columnspan=2, pady=(10,5))
        ttk.Button(left_panel, text="🎫 Book Ticket", command=self.open_booking_window).grid(row=len(labels)+3, column=0, columnspan=2, sticky="ew", padx=20)

        # --- Right Panel: Movie List ---
        right_panel = ttk.LabelFrame(content_frame, text="Movie List", padding=10)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Search Bar
        search_frame = ttk.Frame(right_panel)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(search_frame, text="Search", command=self.search_movie).pack(side=tk.LEFT)
        ttk.Button(search_frame, text="Refresh", command=self.load_movies).pack(side=tk.LEFT, padx=5)

        # Treeview for Data Display
        cols = ("ID", "Name", "Date", "Director", "Cast", "Budget", "Duration", "Rating")
        self.tree = ttk.Treeview(right_panel, columns=cols, show="headings", selectmode="browse")
        
        # Scrollbars
        y_scroll = ttk.Scrollbar(right_panel, orient=tk.VERTICAL, command=self.tree.yview)
        x_scroll = ttk.Scrollbar(right_panel, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscroll=y_scroll.set, xscroll=x_scroll.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=90)
        
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        
        self.load_movies()

    def clear_form(self):
        """Clears all input fields."""
        for var in self.vars.values():
            var.set("")
        self.tree.selection_remove(self.tree.selection())

    def get_form_data(self):
        """Returns a dict of data from inputs."""
        return {k: v.get() for k, v in self.vars.items()}

    def load_movies(self):
        """Fetches movies from DB and populates Treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        movies = self.db.view_movies()
        for movie in movies:
            # Assuming movie tuple: (id, movie_id, name, release, director, cast, budget, duration, rating)
            values = movie[1:] # Skip internal ID
            self.tree.insert("", tk.END, values=values, iid=movie[0])

    def add_movie(self):
        """Adds a movie to the DB."""
        # Validation
        data = self.get_form_data()
        
        if not data["name"] or not data["movie_id"]:
            messagebox.showwarning("Validation Error", "Movie Name and ID are required.")
            return

        # Validate Date
        import re
        if not re.match(r"\d{4}-\d{2}-\d{2}", data["release_date"]):
             messagebox.showwarning("Validation Error", "Date must be in YYYY-MM-DD format.")
             return

        # Validate Numeric Fields
        try:
            float(data["budget"])
            float(data["duration"])
            float(data["rating"])
        except ValueError:
            messagebox.showwarning("Validation Error", "Budget, Duration, and Rating must be numbers.")
            return

        if self.db.add_movie(**data):
            messagebox.showinfo("Success", "Movie added successfully!")
            self.load_movies()
            self.clear_form()
        else:
            messagebox.showerror("Error", "Failed to add movie. Check if Movie ID is unique.")

    def update_movie(self):
        """Updates the selected movie."""
        selected = self.tree.selection()
        if not selected:
             messagebox.showwarning("Warning", "Please select a movie to update.")
             return
        
        internal_id = selected[0]
        if self.db.update_movie(internal_id, **self.get_form_data()):
            messagebox.showinfo("Success", "Movie updated successfully!")
            self.load_movies()
        else:
             messagebox.showerror("Error", "Failed to update movie.")

    def delete_movie(self):
        """Deletes the selected movie."""
        selected = self.tree.selection()
        if not selected:
             messagebox.showwarning("Warning", "Please select a movie to delete.")
             return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this movie?"):
            internal_id = selected[0]
            if self.db.delete_movie(internal_id):
                messagebox.showinfo("Success", "Movie deleted successfully!")
                self.load_movies()
                self.clear_form()
            else:
                messagebox.showerror("Error", "Failed to delete movie.")

    def search_movie(self):
        """Searches movies by name."""
        term = self.search_var.get()
        results = self.db.search_movies(movie_name=term)
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        for movie in results:
             self.tree.insert("", tk.END, values=movie[1:], iid=movie[0])

    def on_select(self, event):
        """Populates form when a row is selected."""
        selected = self.tree.selection()
        if not selected: return
        
        values = self.tree.item(selected[0], 'values')
        # Map values back to variables
        keys = ["movie_id", "name", "release_date", "director", "cast", "budget", "duration", "rating"]
        for i, key in enumerate(keys):
            if i < len(values):
                self.vars[key].set(values[i])

    def open_booking_window(self):
        """Opens the ticket booking modal."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a movie to book.")
            return

        movie_name = self.vars["name"].get()
        
        top = tk.Toplevel(self)
        top.title(f"Book: {movie_name}")
        top.geometry("400x350")
        top.configure(bg="#34495e")

        ttk.Label(top, text=f"Booking for:\n{movie_name}", font=("Segoe UI", 12, "bold"), background="#34495e", foreground="orange", justify="center").pack(pady=20)

        f = ttk.Frame(top)
        f.pack(pady=10)

        # Style for the modal
        style = ttk.Style()
        style.configure("Modal.TLabel", background="#34495e", foreground="white")

        ttk.Label(f, text="Customer Name:", style="Modal.TLabel").grid(row=0, column=0, padx=5, pady=5)
        name_var = tk.StringVar()
        ttk.Entry(f, textvariable=name_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(f, text="No. of Tickets:", style="Modal.TLabel").grid(row=1, column=0, padx=5, pady=5)
        tickets_var = tk.StringVar()
        ttk.Entry(f, textvariable=tickets_var).grid(row=1, column=1, padx=5, pady=5)

        def submit():
            name = name_var.get()
            tickets = tickets_var.get()

            if not name or not tickets:
                messagebox.showerror("Error", "Please fill all fields")
                return
            
            if not tickets.isdigit() or int(tickets) <= 0:
                messagebox.showerror("Error", "Please enter a valid number of tickets.")
                return

            if self.db.add_booking(movie_name, tickets, name):
                messagebox.showinfo("Success", f"Booking Confirmed!\nMovie: {movie_name}\nTickets: {tickets}")
                top.destroy()
            else:
                 messagebox.showerror("Error", "Booking Failed")

        ttk.Button(top, text="Confirm Booking", command=submit).pack(pady=20)

if __name__ == "__main__":
    app = MovieBookingApp()
    app.mainloop()
