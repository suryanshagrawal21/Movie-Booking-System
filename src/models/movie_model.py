from .base_model import BaseModel

class MovieModel(BaseModel):
    def add_movie(self, title, description, release_date, director, cast, budget, duration_minutes, rating, poster_path=None):
        query = """
            INSERT INTO movies (title, description, release_date, director, cast, budget, duration_minutes, rating, poster_path)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        return self.execute_query(query, (title, description, release_date, director, cast, budget, duration_minutes, rating, poster_path))

    def get_all_movies(self):
        return self.fetch_all("SELECT * FROM movies")

    def get_movie_by_id(self, movie_id):
        return self.fetch_one("SELECT * FROM movies WHERE id = %s", (movie_id,))

    def update_movie(self, movie_id, **kwargs):
        if not kwargs: return False
        fields = ", ".join([f"{k} = %s" for k in kwargs.keys()])
        query = f"UPDATE movies SET {fields} WHERE id = %s"
        params = list(kwargs.values()) + [movie_id]
        return self.execute_query(query, params)

    def delete_movie(self, movie_id):
        return self.execute_query("DELETE FROM movies WHERE id = %s", (movie_id,))

    def search_movies(self, term):
        query = "SELECT * FROM movies WHERE title LIKE %s OR description LIKE %s OR cast LIKE %s"
        p = f"%{term}%"
        return self.fetch_all(query, (p, p, p))

    def sync_from_tmdb(self, tmdb_movies):
        """Upserts a list of movies fetched from TMDB into the local database"""
        success_count = 0
        for m in tmdb_movies:
            # We don't have TMDB ID in schema, so we rely on title to avoid duplicates or assume they're fresh
            existing = self.fetch_one("SELECT id FROM movies WHERE title = %s", (m['title'],))
            if not existing:
                try:
                    self.add_movie(
                        title=m['title'],
                        description=m.get('overview', ''),
                        release_date=m.get('release_date', '2000-01-01'),
                        director="TMDB", 
                        cast="",
                        budget=0.0,
                        duration_minutes=120,
                        rating=m.get('vote_average', 0.0),
                        poster_path=m.get('poster_path')
                    )
                    success_count += 1
                except Exception as e:
                    print(f"Error syncing {m['title']}: {e}")
        return success_count
