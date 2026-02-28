import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import mysql.connector
from src.models.base_model import BaseModel
from src.utils.helpers import SecurityUtils
from src.utils.config_manager import ConfigManager
import getpass

def setup_database():
    print("Movie Booking System 2.0 - Database Setup")
    print("-" * 40)
    
    db_instance = BaseModel()
    conn = db_instance._get_connection(db="") # Connect without DB first
    
    if not conn:
        print("[ERROR] Could not connect to MySQL with current settings.")
        host = input("Enter MySQL Host [localhost]: ") or "localhost"
        user = input("Enter MySQL User [root]: ") or "root"
        password = getpass.getpass("Enter MySQL Password: ")
        
        # Test new credentials
        if db_instance.test_connection(host, user, password):
            ConfigManager.update_db_credentials(host, user, password, "movie_booking")
            print("[SUCCESS] Connection successful! Settings saved to config.json.")
            db_instance = BaseModel() # Reload with new config
            conn = db_instance._get_connection(db="")
        else:
            print("[ERROR] Still could not connect. Please check your MySQL service and credentials.")
            return

    cursor = conn.cursor()
    
    # Read and execute schema.sql
    print("Creating schema...")
    schema_path = os.path.join("database", "schema.sql")
    with open(schema_path, 'r') as f:
        schema_sql = f.read()
    
    for query in schema_sql.split(';'):
        if query.strip():
            try:
                cursor.execute(query)
            except Exception as e:
                if "DROP TABLE" not in query:
                    print(f"Warning: {e}")
    
    conn.commit()
    print("[SUCCESS] Schema created successfully.")

    # Seed Initial Data
    print("Seeding initial data...")
    # ... rest of the seeding logic ...
    
    # 1. Admin User
    admin_pass = SecurityUtils.hash_password("admin123")
    cursor.execute("INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)", 
                   ("admin", "admin@movie.com", admin_pass, "admin"))
    
    # 2. Sample Theaters
    theaters = [
        ("Grand Cinema", "Downtown, CityCenter", 100),
        ("Starplex", "Uptown, Business District", 120)
    ]
    cursor.executemany("INSERT INTO theaters (name, location, total_capacity) VALUES (%s, %s, %s)", theaters)
    
    # 3. Seed Movies
    movies = [
        ("Inception", "A thief who steals corporate secrets through the use of dream-sharing technology.", "Christopher Nolan", "Leonardo DiCaprio, Joseph Gordon-Levitt", 148, 8.8, "2010-07-16", "/inception.jpg"),
        ("The Dark Knight", "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham.", "Christopher Nolan", "Christian Bale, Heath Ledger", 152, 9.0, "2008-07-18", "/dark_knight.jpg"),
        ("Interstellar", "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.", "Christopher Nolan", "Matthew McConaughey, Anne Hathaway", 169, 8.6, "2014-11-07", "/interstellar.jpg")
    ]
    cursor.executemany("INSERT INTO movies (title, description, director, cast, duration_minutes, rating, release_date, poster_path) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", movies)
    
    # 4. Sample Shows
    shows = [
        (1, 1, "2026-03-01 18:00:00", 15.00), # Inception at Grand Cinema
        (2, 1, "2026-03-01 20:30:00", 18.00), # The Dark Knight at Grand Cinema
        (3, 2, "2026-03-01 21:00:00", 12.00)  # Interstellar at Starplex
    ]
    cursor.executemany("INSERT INTO shows (movie_id, theater_id, show_time, base_price) VALUES (%s, %s, %s, %s)", shows)
    
    # 5. Sample Seats for Theater 1 (Grand Cinema)
    for row in ['A', 'B', 'C']:
        for num in range(1, 11):
            cursor.execute("INSERT INTO seats (theater_id, row_name, seat_number, is_premium) VALUES (%s, %s, %s, %s)",
                           (1, row, num, row == 'C'))
    
    # 6. Sample Seats for Theater 2 (Starplex)
    for row in ['A', 'B', 'C', 'D']:
        for num in range(1, 13):
            cursor.execute("INSERT INTO seats (theater_id, row_name, seat_number, is_premium) VALUES (%s, %s, %s, %s)",
                           (2, row, num, row == 'D'))

    conn.commit()
    cursor.close()
    conn.close()
    print("Database seeding complete.")

if __name__ == "__main__":
    setup_database()
