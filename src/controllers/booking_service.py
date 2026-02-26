from ..models.movie_model import MovieModel
from ..models.booking_models import ShowModel, TheaterModel, SeatModel, BookingModel
from ..utils.helpers import DocumentUtils
import os

class BookingService:
    def __init__(self):
        self.movie_model = MovieModel()
        self.show_model = ShowModel()
        self.theater_model = TheaterModel()
        self.seat_model = SeatModel()
        self.booking_model = BookingModel()

    def get_available_movies(self):
        return self.movie_model.get_all_movies()

    def get_shows_for_movie(self, movie_id):
        return self.show_model.get_shows_by_movie(movie_id)

    def get_seats_for_show(self, show_id):
        """Returns all seats for a show with their availability status."""
        show = self.show_model.get_show_details(show_id)
        if not show: return []
        
        all_seats = self.seat_model.get_seats_by_theater(show['theater_id'])
        available_seats = self.seat_model.get_available_seats(show_id)
        available_ids = [s['id'] for s in available_seats]
        
        for seat in all_seats:
            seat['is_available'] = seat['id'] in available_ids
            
        return all_seats

    def book_tickets(self, user_id, show_id, seat_ids):
        """Processes a booking with multiple seats."""
        show = self.show_model.get_show_details(show_id)
        if not show: return False, "Show not found."
        
        # Calculate total price (could include premium seat logic)
        total_price = float(show['base_price']) * len(seat_ids)
        
        success, result = self.booking_model.create_booking(user_id, show_id, seat_ids, total_price)
        
        if success:
            booking_id = result
            # Generate Ticket
            booking_details = {
                "id": booking_id,
                "movie_title": show['movie_title'],
                "theater_name": show['theater_name'],
                "show_time": show['show_time'],
                "total_tickets": len(seat_ids),
                "total_price": total_price
            }
            
            # Ensure tickets directory exists
            if not os.path.exists("tickets"):
                os.makedirs("tickets")
                
            ticket_path = f"tickets/ticket_{booking_id}.pdf"
            DocumentUtils.generate_ticket_pdf(booking_details, ticket_path)
            
            return True, ticket_path
        
        return False, result # result contains the error message

    def get_user_history(self, user_id):
        return self.booking_model.get_user_booking_history(user_id)
