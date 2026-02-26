from ..models.movie_model import MovieModel
from ..models.booking_models import ShowModel, TheaterModel
from ..utils.helpers import DocumentUtils
import os

class BookingService:
    def __init__(self):
        self.movie_model = MovieModel()
        self.show_model = ShowModel()
        self.theater_model = TheaterModel()

    def get_available_movies(self):
        return self.movie_model.get_all_movies()

    def get_shows_for_movie(self, movie_id):
        return self.show_model.get_shows_by_movie(movie_id)

    def book_tickets(self, user_id, show_id, ticket_count):
        # Placeholder for complex seat selection logic
        # For now, just create a booking entry
        show = self.show_model.get_show_details(show_id)
        if not show: return False, "Show not found."
        
        total_price = float(show['base_price']) * ticket_count
        
        query = "INSERT INTO bookings (user_id, show_id, total_tickets, total_price) VALUES (%s, %s, %s, %s)"
        db = self.movie_model # Reuse model connection logic
        if db.execute_query(query, (user_id, show_id, ticket_count, total_price)):
            booking_id = db.fetch_one("SELECT LAST_INSERT_ID() as id")['id']
            
            # Generate Ticket
            booking_details = {
                "id": booking_id,
                "movie_title": show['movie_title'],
                "theater_name": show['theater_name'],
                "show_time": show['show_time'],
                "total_tickets": ticket_count,
                "total_price": total_price
            }
            ticket_path = f"tickets/ticket_{booking_id}.pdf"
            DocumentUtils.generate_ticket_pdf(booking_details, ticket_path)
            
            return True, ticket_path
        
        return False, "Booking failed."
