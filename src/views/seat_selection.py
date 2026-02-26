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
        self.info_frame.pack(fill="x", padx=40, pady=(30, 10))
        
        self.movie_label = ctk.CTkLabel(self.info_frame, text=self.movie['title'].upper(), font=ctk.CTkFont(size=28, weight="bold"), text_color="#c0392b")
        self.movie_label.pack(side="left")
        
        self.show_label = ctk.CTkLabel(self.info_frame, text=f"{self.show['show_time']} | {self.show['theater_name']}", font=ctk.CTkFont(size=14), text_color="#888888")
        self.show_label.pack(side="right")

        # Screen Indicator with Glow
        self.screen_frame = ctk.CTkFrame(self, height=10, fg_color="#c0392b", corner_radius=5)
        self.screen_frame.pack(fill="x", padx=100, pady=(30, 10))
        ctk.CTkLabel(self, text="SCREEN", font=ctk.CTkFont(size=12, weight="bold"), text_color="#555555").pack()
        
        # Scrollable Seat Area
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        self.grid_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.grid_frame.pack(pady=20)

        # Legend
        self.legend_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.legend_frame.pack(pady=10)
        
        self.create_legend("AVAILABLE", "#27ae60")
        self.create_legend("OCCUPIED", "#555555")
        self.create_legend("SELECTED", "#f39c12")

        # Bottom Bar
        self.bottom_bar = ctk.CTkFrame(self, height=100, corner_radius=0, fg_color="#1a1a1a")
        self.bottom_bar.pack(fill="x", side="bottom")
        
        self.status_label = ctk.CTkLabel(self.bottom_bar, text="Selected: 0 seats | Total: $0.00", font=ctk.CTkFont(size=16, weight="bold"))
        self.status_label.pack(side="left", padx=40, pady=20)
        
        self.confirm_btn = ctk.CTkButton(
            self.bottom_bar, text="CONFIRM BOOKING", 
            width=200, height=45, corner_radius=8,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.confirm_booking, state="disabled"
        )
        self.confirm_btn.pack(side="right", padx=40, pady=20)

    def create_legend(self, text, color):
        f = ctk.CTkFrame(self.legend_frame, fg_color="transparent")
        f.pack(side="left", padx=15)
        ctk.CTkFrame(f, width=15, height=15, fg_color=color, corner_radius=2).pack(side="left", padx=5)
        ctk.CTkLabel(f, text=text, font=ctk.CTkFont(size=11, weight="bold"), text_color="#888888").pack(side="left")

    def load_seats(self):
        seats = self.booking_service.get_seats_for_show(self.show['id'])
        
        rows = {}
        for s in seats:
            if s['row_name'] not in rows:
                rows[s['row_name']] = []
            rows[s['row_name']].append(s)
            
        for r_idx, (row_name, row_seats) in enumerate(sorted(rows.items())):
            ctk.CTkLabel(self.grid_frame, text=row_name, width=30, font=ctk.CTkFont(weight="bold")).grid(row=r_idx, column=0, padx=10)
            for c_idx, seat in enumerate(sorted(row_seats, key=lambda x: x['seat_number'])):
                color = "#27ae60" if seat['is_available'] else "#555555"
                state = "normal" if seat['is_available'] else "disabled"
                hover = "#2ecc71" if seat['is_available'] else "#555555"
                
                btn = ctk.CTkButton(
                    self.grid_frame, 
                    text=str(seat['seat_number']), 
                    width=45, height=45, corner_radius=6,
                    fg_color=color,
                    hover_color=hover,
                    state=state,
                    font=ctk.CTkFont(size=12, weight="bold"),
                    command=lambda s=seat: self.toggle_seat(s)
                )
                btn.grid(row=r_idx, column=c_idx + 1, padx=4, pady=4)
                seat['btn'] = btn

    def toggle_seat(self, seat):
        seat_id = seat['id']
        seat_name = f"{seat['row_name']}{seat['seat_number']}"
        
        if seat_id in self.selected_seats:
            del self.selected_seats[seat_id]
            seat['btn'].configure(fg_color="#27ae60")
        else:
            self.selected_seats[seat_id] = seat_name
            seat['btn'].configure(fg_color="#f39c12")
        
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
