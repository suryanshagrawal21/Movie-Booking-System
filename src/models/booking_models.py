from .base_model import BaseModel

class TheaterModel(BaseModel):
    def add_theater(self, name, location, total_capacity):
        query = "INSERT INTO theaters (name, location, total_capacity) VALUES (%s, %s, %s)"
        return self.execute_query(query, (name, location, total_capacity))

    def get_all_theaters(self):
        return self.fetch_all("SELECT * FROM theaters")

class ShowModel(BaseModel):
    def add_show(self, movie_id, theater_id, show_time, base_price):
        query = "INSERT INTO shows (movie_id, theater_id, show_time, base_price) VALUES (%s, %s, %s, %s)"
        return self.execute_query(query, (movie_id, theater_id, show_time, base_price))

    def get_shows_by_movie(self, movie_id):
        query = """
            SELECT s.*, t.name as theater_name, t.location 
            FROM shows s 
            JOIN theaters t ON s.theater_id = t.id 
            WHERE s.movie_id = %s AND s.show_time > NOW()
        """
        return self.fetch_all(query, (movie_id,))
    
    def get_show_details(self, show_id):
        query = """
            SELECT s.*, m.title as movie_title, t.name as theater_name 
            FROM shows s 
            JOIN movies m ON s.movie_id = m.id 
            JOIN theaters t ON s.theater_id = t.id 
            WHERE s.id = %s
        """
        return self.fetch_one(query, (show_id,))

class SeatModel(BaseModel):
    def get_seats_by_theater(self, theater_id):
        query = "SELECT * FROM seats WHERE theater_id = %s ORDER BY row_name, seat_number"
        return self.fetch_all(query, (theater_id,))

    def get_available_seats(self, show_id):
        """Returns seats that are NOT yet booked for a specific show."""
        query = """
            SELECT s.* FROM seats s
            JOIN shows sh ON s.theater_id = sh.theater_id
            WHERE sh.id = %s
            AND s.id NOT IN (
                SELECT bs.seat_id FROM booking_seats bs
                JOIN bookings b ON bs.booking_id = b.id
                WHERE b.show_id = %s
            )
        """
        return self.fetch_all(query, (show_id, show_id))

class BookingModel(BaseModel):
    def create_booking(self, user_id, show_id, seat_ids, total_price):
        """
        Handles booking creation and seat association.
        Ideally should be transactional. 
        Note: BaseModel.execute_query currently closes connection after each call.
        I will implement a custom transactional method here.
        """
        conn = self._get_connection()
        if not conn: return False, "Database connection failed"
        
        try:
            cursor = conn.cursor()
            conn.start_transaction()
            
            # 1. Create Booking
            cursor.execute(
                "INSERT INTO bookings (user_id, show_id, total_tickets, total_price) VALUES (%s, %s, %s, %s)",
                (user_id, show_id, len(seat_ids), total_price)
            )
            booking_id = cursor.lastrowid
            
            # 2. Associate Seats
            for seat_id in seat_ids:
                # Check if seat is still available (Atomic check)
                check_query = """
                    SELECT 1 FROM booking_seats bs
                    JOIN bookings b ON bs.booking_id = b.id
                    WHERE b.show_id = %s AND bs.seat_id = %s
                """
                cursor.execute(check_query, (show_id, seat_id))
                if cursor.fetchone():
                    conn.rollback()
                    return False, f"Seat {seat_id} was just taken by another user."
                
                cursor.execute(
                    "INSERT INTO booking_seats (booking_id, seat_id) VALUES (%s, %s)",
                    (booking_id, seat_id)
                )
            
            conn.commit()
            return True, booking_id
        except Exception as e:
            conn.rollback()
            return False, str(e)
        finally:
            cursor.close()
            conn.close()

    def get_user_booking_history(self, user_id):
        query = """
            SELECT b.*, m.title as movie_title, s.show_time, t.name as theater_name
            FROM bookings b
            JOIN shows s ON b.show_id = s.id
            JOIN movies m ON s.movie_id = m.id
            JOIN theaters t ON s.theater_id = t.id
            WHERE b.user_id = %s
            ORDER BY b.booking_time DESC
        """
        return self.fetch_all(query, (user_id,))

    def get_all_bookings(self):
        """Fetches all bookings for admin view."""
        query = """
            SELECT b.*, u.username, m.title as movie_title, s.show_time, t.name as theater_name
            FROM bookings b
            JOIN users u ON b.user_id = u.id
            JOIN shows s ON b.show_id = s.id
            JOIN movies m ON s.movie_id = m.id
            JOIN theaters t ON s.theater_id = t.id
            ORDER BY b.booking_time DESC
        """
        return self.fetch_all(query)
