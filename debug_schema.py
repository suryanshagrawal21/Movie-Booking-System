import mysql.connector
from src.database import DatabaseManager

def fix_schema():
    print("Checking database schema...")
    db = DatabaseManager(password="Divya.21")
    
    if not db.connect():
        print("Could not connect to database with default password.")
        # Simple retry logic or just fail for this debug script
        return

    try:
        cursor = db.conn.cursor()
        
        # Check columns in movies table
        print("Describing 'movies' table:")
        try:
            cursor.execute("DESCRIBE movies")
            columns = [row[0] for row in cursor.fetchall()]
            print(f"Columns: {columns}")
            
            if "movie_id" not in columns:
                print("CRITICAL: 'movie_id' column is MISSING.")
                print("Re-creating table...")
                cursor.execute("DROP TABLE IF EXISTS movies")
                cursor.execute("DROP TABLE IF EXISTS bookings")
                
                # Re-read schema.sql
                with open("database/schema.sql", "r") as f:
                    schema_sql = f.read()
                
                for result in cursor.execute(schema_sql, multi=True):
                     if result.with_rows: result.fetchall()
                print("Tables re-created successfully.")
                
            else:
                print("'movie_id' column exists.")
                
        except mysql.connector.Error as err:
            print(f"Error describing table: {err}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    fix_schema()
