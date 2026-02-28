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

        # Screen Indicator with Glow (Curved Effect Simulation)
        self.screen_container = ctk.CTkFrame(self, fg_color="transparent")
        self.screen_container.pack(fill="x", padx=100, pady=(20, 10))
        
        # Fake a curve using a canvas
        self.screen_canvas = ctk.CTkCanvas(self.screen_container, height=40, bg="#1a1a1a", highlightthickness=0)
        self.screen_canvas.pack(fill="x")
        self.screen_canvas.bind("<Configure>", self.draw_curved_screen)
        
        # Scrollable Seat Area
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.grid_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.grid_frame.pack(pady=10)

        # Legend
        self.legend_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.legend_frame.pack(pady=10)
        
        self.create_legend("AVAILABLE", "#2ecc71")
        self.create_legend("PREMIUM", "#9b59b6")
        self.create_legend("OCCUPIED", "#333333")
        self.create_legend("SELECTED", "#e67e22")

        # Bottom Bar
        self.bottom_bar = ctk.CTkFrame(self, height=80, corner_radius=15, fg_color="#111111", border_width=1, border_color="#333333")
        self.bottom_bar.pack(fill="x", side="bottom", padx=20, pady=20)
        
        self.status_label = ctk.CTkLabel(self.bottom_bar, text="Selected: 0 seats | Total: $0.00", font=ctk.CTkFont(size=16, weight="bold"), text_color="#f1f1f1")
        self.status_label.pack(side="left", padx=40, pady=20)
        
        self.confirm_btn = ctk.CTkButton(
            self.bottom_bar, text="PROCEED TO PAY", 
            width=200, height=45, corner_radius=8,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#e50914", hover_color="#b80710",
            command=self.simulate_payment, state="disabled"
        )
        self.confirm_btn.pack(side="right", padx=40, pady=20)

    def draw_curved_screen(self, event):
        self.screen_canvas.delete("all")
        w = event.width
        h = event.height
        # Draw curved line for screen
        self.screen_canvas.create_arc(10, -h*2, w-10, h-5, start=180, extent=180, style="arc", outline="#e50914", width=3)
        self.screen_canvas.create_text(w/2, h/2 + 10, text="SCREEN", fill="#888888", font=("Inter", 10, "bold"))

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
                is_premium = seat.get('is_premium', False)
                base_color = "#9b59b6" if is_premium else "#2ecc71"
                
                color = base_color if seat['is_available'] else "#333333"
                state = "normal" if seat['is_available'] else "disabled"
                hover = "#8e44ad" if is_premium else "#27ae60"
                if not seat['is_available']: hover = "#333333"
                
                btn = ctk.CTkButton(
                    self.grid_frame, 
                    text=str(seat['seat_number']), 
                    width=40, height=40, corner_radius=8,
                    fg_color=color, hover_color=hover, state=state,
                    font=ctk.CTkFont(size=12, weight="bold"),
                    command=lambda s=seat, bc=base_color: self.toggle_seat(s, bc)
                )
                btn.grid(row=r_idx, column=c_idx + 1, padx=6, pady=6)
                seat['btn'] = btn

    def toggle_seat(self, seat, base_color):
        seat_id = seat['id']
        seat_name = f"{seat['row_name']}{seat['seat_number']}"
        
        if seat_id in self.selected_seats:
            del self.selected_seats[seat_id]
            seat['btn'].configure(fg_color=base_color)
        else:
            self.selected_seats[seat_id] = seat_name
            seat['btn'].configure(fg_color="#e67e22") # Selected color
        
        count = len(self.selected_seats)
        
        # Calculate true price including premium markup
        total_price = 0
        for s_id in self.selected_seats:
            st = next(s for s in self.booking_service.get_seats_for_show(self.show['id']) if s['id'] == s_id)
            p = float(self.show['base_price'])
            if st.get('is_premium'): p += 5.0 # Premium markup
            total_price += p
            
        self.status_label.configure(text=f"Selected: {count} seats | Total: ${total_price:.2f}")
        self.confirm_btn.configure(state="normal" if count > 0 else "disabled")

    def simulate_payment(self):
        if not self.selected_seats: return
        
        self.confirm_btn.configure(text="Processing...", state="disabled")
        
        # Show payment modal
        pay_win = ctk.CTkToplevel(self)
        pay_win.title("Secure Payment")
        pay_win.geometry("350x450")
        pay_win.attributes("-topmost", True)
        
        ctk.CTkLabel(pay_win, text="Payment Gateway", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        
        card_frame = ctk.CTkFrame(pay_win, fg_color="#222", corner_radius=10)
        card_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        count = len(self.selected_seats)
        total_price = 0
        for s_id in self.selected_seats:
            st = next(s for s in self.booking_service.get_seats_for_show(self.show['id']) if s['id'] == s_id)
            p = float(self.show['base_price'])
            if st.get('is_premium'): p += 5.0
            total_price += p
            
        ctk.CTkLabel(card_frame, text=f"Amount Due: ${total_price:.2f}", font=ctk.CTkFont(size=24, weight="bold"), text_color="#2ecc71").pack(pady=30)
        
        ctk.CTkEntry(card_frame, placeholder_text="Card Number", width=250).pack(pady=10)
        
        row = ctk.CTkFrame(card_frame, fg_color="transparent")
        row.pack(pady=10)
        ctk.CTkEntry(row, placeholder_text="MM/YY", width=120).pack(side="left", padx=5)
        ctk.CTkEntry(row, placeholder_text="CVV", width=120, show="*").pack(side="left", padx=5)
        
        def process():
            pay_win.destroy()
            self.confirm_booking()
            
        ctk.CTkButton(card_frame, text="Pay Now", command=process, width=250, height=45, fg_color="#27ae60").pack(pady=30)

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
