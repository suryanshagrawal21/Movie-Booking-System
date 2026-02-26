import mysql.connector
from src.models.base_model import BaseModel
from src.utils.helpers import SecurityUtils
from src.utils.config_manager import ConfigManager
import os
import getpass

def setup_database():
    print("🎬 Movie Booking System 2.0 - Database Setup")
    print("-" * 40)
    
    db = BaseModel()
    conn = db._get_connection(database="") # Connect without DB first
    
    if not conn:
        print("❌ Could not connect to MySQL with current settings.")
        host = input("Enter MySQL Host [localhost]: ") or "localhost"
        user = input("Enter MySQL User [root]: ") or "root"
        password = getpass.getpass("Enter MySQL Password: ")
        
        # Test new credentials
        if db.test_connection(host, user, password):
            ConfigManager.update_db_credentials(host, user, password, "movie_booking")
            print("✅ Connection successful! Settings saved to config.json.")
            db = BaseModel() # Reload with new config
            conn = db._get_connection(database="")
        else:
            print("❌ Still could not connect. Please check your MySQL service and credentials.")
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
    print("✅ Schema created successfully.")

    # Seed Initial Data
    print("Seeding initial data...")
    # ... rest of the seeding logic ...
    
    # 1. Admin User
    admin_pass = SecurityUtils.hash_password("admin123")
    cursor.execute("INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)", 
                   ("admin", "admin@movie.com", admin_pass, "admin"))
    
    # 2. Sample Theater
    cursor.execute("INSERT INTO theaters (name, location, total_capacity) VALUES (%s, %s, %s)",
                   ("Grand Cinema", "Downtown, CityCenter", 100))
    theater_id = cursor.lastrowid
    
    # 3. Sample Movie
    cursor.execute("""
        INSERT INTO movies (title, description, release_date, director, cast, budget, duration_minutes, rating) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
        ("Inception", "A thief who steals corporate secrets through the use of dream-sharing technology.", 
         "2010-07-16", "Christopher Nolan", "Leonardo DiCaprio, Joseph Gordon-Levitt", 160000000, 148, 8.8))
    movie_id = cursor.lastrowid
    
    # 4. Sample Show
    cursor.execute("INSERT INTO shows (movie_id, theater_id, show_time, base_price) VALUES (%s, %s, %s, %s)",
                   (movie_id, theater_id, "2026-03-01 18:00:00", 12.50))
    
    # 5. Sample Seats
    for row in ['A', 'B', 'C']:
        for num in range(1, 11):
            cursor.execute("INSERT INTO seats (theater_id, row_name, seat_number, is_premium) VALUES (%s, %s, %s, %s)",
                           (theater_id, row, num, row == 'C'))

    conn.commit()
    cursor.close()
    conn.close()
    print("Database seeding complete.")

if __name__ == "__main__":
    setup_database()
