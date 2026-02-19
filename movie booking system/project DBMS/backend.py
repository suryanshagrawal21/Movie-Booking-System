import mysql.connector
from mysql.connector import Error

class DatabaseManager:
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
        try:
            self.conn = mysql.connector.connect(**self.config)
            if self.conn.is_connected():
                self.cursor = self.conn.cursor()
                return True
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return False

    def close(self):
        if self.conn and self.conn.is_connected():
            self.cursor.close()
            self.conn.close()

    def execute_query(self, query, params=None):
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
        query = """
        INSERT INTO movies (movie_id, movie_name, release_date, director, cast, budget, duration, rating)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        return self.execute_query(query, (movie_id, name, release_date, director, cast, budget, duration, rating))

    def view_movies(self):
        return self.fetch_all("SELECT * FROM movies")

    def delete_movie(self, id):
        return self.execute_query("DELETE FROM movies WHERE id = %s", (id,))

    def update_movie(self, id, movie_id, name, release_date, director, cast, budget, duration, rating):
        query = """
        UPDATE movies SET movie_id=%s, movie_name=%s, release_date=%s, director=%s, cast=%s, 
        budget=%s, duration=%s, rating=%s WHERE id=%s
        """
        return self.execute_query(query, (movie_id, name, release_date, director, cast, budget, duration, rating, id))

    def search_movies(self, **kwargs):
        # Construct dynamic query based on non-empty create_args
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
        return self.execute_query(
            "INSERT INTO bookings (movie_name, num_tickets, customer_name) VALUES (%s, %s, %s)",
            (movie_name, num_tickets, customer_name)
        )
