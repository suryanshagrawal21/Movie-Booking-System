import mysql.connector
from mysql.connector import Error

class DatabaseManager:
    """
    Manages database connections and operations for the Movie Booking System.
    """
    def __init__(self, host="localhost", user="root", password="password", database="movie_booking"):
        self.config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database
        }
        self.conn = None
        self.cursor = None

    def connect(self):
        """
        Establishes a connection to the MySQL database.
        Returns:
            bool: True if connection successful, False otherwise.
        """
        try:
            self.conn = mysql.connector.connect(**self.config)
            if self.conn.is_connected():
                self.cursor = self.conn.cursor()
                return True
        except Error as e:
            # print(f"Error connecting to MySQL: {e}") # Suppress for cleaner UI, handled by caller
            return False

    def close(self):
        """Closes the database connection."""
        if self.conn and self.conn.is_connected():
            self.cursor.close()
            self.conn.close()

    def execute_query(self, query, params=None):
        """
        Executes a query (INSERT, UPDATE, DELETE).
        Args:
            query (str): SQL query.
            params (tuple, optional): Parameters for the query.
        Returns:
            bool: True if successful, False otherwise.
        """
        if self.connect():
            try:
                if params:
                    self.cursor.execute(query, params)
                else:
                    self.cursor.execute(query)
                self.conn.commit()
                return True
            except Error as e:
                print(f"Error executing query: {e}")
                return False
            finally:
                self.close()
        return False

    def fetch_all(self, query, params=None):
        """
        Executes a SELECT query and returns all results.
        Args:
            query (str): SQL query.
            params (tuple, optional): Parameters.
        Returns:
            list: List of tuples representing rows.
        """
        if self.connect():
            try:
                if params:
                    self.cursor.execute(query, params)
                else:
                    self.cursor.execute(query)
                return self.cursor.fetchall()
            except Error as e:
                print(f"Error fetching data: {e}")
                return []
            finally:
                self.close()
        return []

    # --- Specific Operations ---

    def add_movie(self, movie_id, name, release_date, director, cast, budget, duration, rating):
        """Adds a new movie to the database."""
        query = """
        INSERT INTO movies (movie_id, movie_name, release_date, director, cast, budget, duration, rating)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        return self.execute_query(query, (movie_id, name, release_date, director, cast, budget, duration, rating))

    def view_movies(self):
        """Retrieves all movies."""
        return self.fetch_all("SELECT * FROM movies")

    def delete_movie(self, id):
        """Deletes a movie by its internal ID."""
        return self.execute_query("DELETE FROM movies WHERE id = %s", (id,))

    def update_movie(self, id, movie_id, name, release_date, director, cast, budget, duration, rating):
        """Updates an existing movie record."""
        query = """
        UPDATE movies SET movie_id=%s, movie_name=%s, release_date=%s, director=%s, cast=%s, 
        budget=%s, duration=%s, rating=%s WHERE id=%s
        """
        return self.execute_query(query, (movie_id, name, release_date, director, cast, budget, duration, rating, id))

    def search_movies(self, **kwargs):
        """
        Searches for movies based on provided criteria (keyword arguments).
        Example: search_movies(movie_name="Inception")
        """
        conditions = []
        params = []
        for key, value in kwargs.items():
            if value:
                conditions.append(f"{key} LIKE %s")
                params.append(f"%{value}%")
        
        if not conditions:
            return self.view_movies()
        
        query = f"SELECT * FROM movies WHERE {' AND '.join(conditions)}"
        return self.fetch_all(query, tuple(params))

    def add_booking(self, movie_name, num_tickets, customer_name):
        """Adds a booking record."""
        return self.execute_query(
            "INSERT INTO bookings (movie_name, num_tickets, customer_name) VALUES (%s, %s, %s)",
            (movie_name, num_tickets, customer_name)
        )
