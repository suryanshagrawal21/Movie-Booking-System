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
