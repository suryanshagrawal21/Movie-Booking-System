import customtkinter as ctk

class SeatSelectionView(ctk.CTkToplevel):
    def __init__(self, master, movie, show, booking_service, on_booking_complete):
        super().__init__(master)
        self.title(f"Select Seats - {movie['title']}")
        self.geometry("600x600")
        
        self.movie = movie
        self.show = show
        self.booking_service = booking_service
        self.on_booking_complete = on_booking_complete
        
        self.selected_seats = []
        self.setup_ui()

    def setup_ui(self):
        self.label = ctk.CTkLabel(self, text="Screen This Way", fg_color="gray30", height=40, corner_radius=5)
        self.label.pack(fill="x", padx=40, pady=20)
        
        self.grid_frame = ctk.CTkFrame(self)
        self.grid_frame.pack(pady=20)
        
        # Create a 5x10 grid of seats as a sample
        rows = ['A', 'B', 'C', 'D', 'E']
        for r_idx, row in enumerate(rows):
            ctk.CTkLabel(self.grid_frame, text=row, width=30).grid(row=r_idx, column=0, padx=5)
            for c_idx in range(1, 11):
                btn = ctk.CTkButton(self.grid_frame, text=str(c_idx), width=40, height=40, 
                                    fg_color="green", hover_color="darkgreen",
                                    command=lambda r=row, c=c_idx: self.toggle_seat(r, c))
                btn.grid(row=r_idx, column=c_idx, padx=2, pady=2)

        self.info_label = ctk.CTkLabel(self, text="Selected: 0 seats | Total: $0.00")
        self.info_label.pack(pady=10)
        
        self.confirm_btn = ctk.CTkButton(self, text="Confirm Booking", command=self.confirm_booking)
        self.confirm_btn.pack(pady=20)

    def toggle_seat(self, row, col):
        seat = f"{row}{col}"
        if seat in self.selected_seats:
            self.selected_seats.remove(seat)
        else:
            self.selected_seats.append(seat)
        
        price = len(self.selected_seats) * float(self.show['base_price'])
        self.info_label.configure(text=f"Selected: {len(self.selected_seats)} seats | Total: ${price:.2f}")

    def confirm_booking(self):
        if not self.selected_seats:
            return
        
        success, message = self.booking_service.book_tickets(
            user_id=self.master.auth_service.current_user['id'], 
            show_id=self.show['id'], 
            ticket_count=len(self.selected_seats)
        )
        
        if success:
            self.on_booking_complete(message)
            self.destroy()
        else:
            print(f"Booking error: {message}")
