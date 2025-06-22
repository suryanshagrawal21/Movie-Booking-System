import mysql.connector

# Connect to MySQL
def connect():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",          # Update as needed
        password="Divya.21",  # Update as needed
        database="movie_booking"
    )
    return conn

# Add a movie
def AddMovieRec(movie_id, name, release_date, director, cast, budget, duration, rating):
    conn = connect()
    cursor = conn.cursor()
    query = """
    INSERT INTO movies (movie_id, movie_name, release_date, director, cast, budget, duration, rating)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (movie_id, name, release_date, director, cast, budget, duration, rating))
    conn.commit()
    conn.close()

# View all movies
def ViewMovieData():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Delete movie by ID
def DeleteMovieRec(id):
    conn = connect()
    cursor = conn.cursor()
    query = "DELETE FROM movies WHERE id = %s"
    cursor.execute(query, (id,))
    conn.commit()
    conn.close()

# Update movie record
def UpdateMovieRec(id, movie_id, name, release_date, director, cast, budget, duration, rating):
    conn = connect()
    cursor = conn.cursor()
    query = """
    UPDATE movies SET movie_id=%s, movie_name=%s, release_date=%s, director=%s, cast=%s, 
    budget=%s, duration=%s, rating=%s WHERE id=%s
    """
    cursor.execute(query, (movie_id, name, release_date, director, cast, budget, duration, rating, id))
    conn.commit()
    conn.close()

# Search movies
def SearchMovieData(movie_id="", name="", release_date="", director="", cast="", budget="", duration="", rating=""):
    conn = connect()
    cursor = conn.cursor()
    query = """
    SELECT * FROM movies WHERE 
    movie_id LIKE %s AND movie_name LIKE %s AND release_date LIKE %s AND 
    director LIKE %s AND cast LIKE %s AND budget LIKE %s AND duration LIKE %s AND rating LIKE %s
    """
    cursor.execute(query, (
        f"%{movie_id}%", f"%{name}%", f"%{release_date}%", f"%{director}%",
        f"%{cast}%", f"%{budget}%", f"%{duration}%", f"%{rating}%"
    ))
    rows = cursor.fetchall()
    conn.close()
    return rows

# Add a ticket booking
def AddBooking(movie_name, num_tickets, customer_name):
    conn = connect()
    cursor = conn.cursor()
    query = "INSERT INTO bookings (movie_name, num_tickets, customer_name) VALUES (%s, %s, %s)"
    cursor.execute(query, (movie_name, num_tickets, customer_name))
    conn.commit()
    conn.close()
