import customtkinter as ctk
from tkinter import messagebox

class SeatSelectionView(ctk.CTkToplevel):
    def __init__(self, master, movie, show, booking_service, on_booking_complete):
        super().__init__(master)
        self.title(f"Select Seats - {movie['title']}")
        self.geometry("800x700")
        
        self.movie = movie
        self.show = show
        self.booking_service = booking_service
        self.on_booking_complete = on_booking_complete
        
        self.selected_seats = {} # id: name
        self.setup_ui()
        self.load_seats()

    def setup_ui(self):
        # Header Info
        self.info_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.info_frame.pack(fill="x", padx=40, pady=(20, 10))
        
        self.movie_label = ctk.CTkLabel(self.info_frame, text=self.movie['title'], font=ctk.CTkFont(size=24, weight="bold"))
        self.movie_label.pack(side="left")
        
        self.show_label = ctk.CTkLabel(self.info_frame, text=f"Show: {self.show['show_time']} | {self.show['theater_name']}", font=ctk.CTkFont(size=14))
        self.show_label.pack(side="right")

        # Screen Indicator
        self.screen_label = ctk.CTkLabel(self, text="SCREEN", fg_color="gray30", height=10, corner_radius=2)
        self.screen_label.pack(fill="x", padx=100, pady=20)
        
        # Scrollable Seat Area
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.grid_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.grid_frame.pack(pady=20)

        # Bottom Bar
        self.bottom_bar = ctk.CTkFrame(self, height=100)
        self.bottom_bar.pack(fill="x", side="bottom", padx=20, pady=20)
        
        self.status_label = ctk.CTkLabel(self.bottom_bar, text="Selected: 0 seats | Total: $0.00", font=ctk.CTkFont(size=14, weight="bold"))
        self.status_label.pack(side="left", padx=20)
        
        self.confirm_btn = ctk.CTkButton(self.bottom_bar, text="Confirm Booking", command=self.confirm_booking, state="disabled")
        self.confirm_btn.pack(side="right", padx=20)

        # Legend
        self.legend_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.legend_frame.pack(pady=5)
        
        self.create_legend("Available", "green")
        self.create_legend("Occupied", "red")
        self.create_legend("Selected", "orange")

    def create_legend(self, text, color):
        f = ctk.CTkFrame(self.legend_frame, fg_color="transparent")
        f.pack(side="left", padx=10)
        ctk.CTkFrame(f, width=15, height=15, fg_color=color).pack(side="left", padx=5)
        ctk.CTkLabel(f, text=text, font=ctk.CTkFont(size=10)).pack(side="left")

    def load_seats(self):
        seats = self.booking_service.get_seats_for_show(self.show['id'])
        
        # Group seats by row
        rows = {}
        for s in seats:
            if s['row_name'] not in rows:
                rows[s['row_name']] = []
            rows[s['row_name']].append(s)
            
        for r_idx, (row_name, row_seats) in enumerate(sorted(rows.items())):
            ctk.CTkLabel(self.grid_frame, text=row_name, width=30).grid(row=r_idx, column=0, padx=5)
            for c_idx, seat in enumerate(sorted(row_seats, key=lambda x: x['seat_number'])):
                color = "green" if seat['is_available'] else "red"
                state = "normal" if seat['is_available'] else "disabled"
                
                # Highlight premium seats
                hover = "darkgreen" if seat['is_available'] else "red"
                
                btn = ctk.CTkButton(
                    self.grid_frame, 
                    text=str(seat['seat_number']), 
                    width=40, height=40, 
                    fg_color=color,
                    hover_color=hover,
                    state=state,
                    command=lambda s=seat: self.toggle_seat(s)
                )
                btn.grid(row=r_idx, column=c_idx + 1, padx=2, pady=2)
                seat['btn'] = btn

    def toggle_seat(self, seat):
        seat_id = seat['id']
        seat_name = f"{seat['row_name']}{seat['seat_number']}"
        
        if seat_id in self.selected_seats:
            del self.selected_seats[seat_id]
            seat['btn'].configure(fg_color="green")
        else:
            self.selected_seats[seat_id] = seat_name
            seat['btn'].configure(fg_color="orange")
        
        count = len(self.selected_seats)
        price = count * float(self.show['base_price'])
        self.status_label.configure(text=f"Selected: {count} seats | Total: ${price:.2f}")
        self.confirm_btn.configure(state="normal" if count > 0 else "disabled")

    def confirm_booking(self):
        if not self.selected_seats: return
        
        if not messagebox.askyesno("Confirm", f"Book {len(self.selected_seats)} tickets?"):
            return
            
        success, result = self.booking_service.book_tickets(
            user_id=self.master.user['id'], 
            show_id=self.show['id'], 
            seat_ids=list(self.selected_seats.keys())
        )
        
        if success:
            self.on_booking_complete(result)
            self.destroy()
        else:
            messagebox.showerror("Error", f"Booking failed: {result}")
