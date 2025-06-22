# 🎬 Online Movie Ticket Booking System
This is a GUI-based application developed using Python Tkinter and MySQL to manage movie details and book tickets online. The project provides an easy-to-use interface for adding, updating, deleting, and searching movie data, as well as booking tickets for selected movies.

# 📌 Features
- Add new movie details (ID, name, release date, director, cast, etc.)
- View all movies in a list
- Search for movies using any field
- Update or delete selected movie entries
- Book tickets by entering customer name and number of tickets
- Uses MySQL for backend storage

# 🛠️ Tech Stack
Frontend: Python Tkinter
Backend: MySQL Database
Language: Python 3

# 💾 Database Structure
Make sure you have a MySQL database called movie_booking with the following tables:

CREATE TABLE movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id VARCHAR(20),
    movie_name VARCHAR(100),
    release_date DATE,
    director VARCHAR(100),
    cast TEXT,
    budget VARCHAR(50),
    duration VARCHAR(50),
    rating VARCHAR(10)
);

CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_name VARCHAR(100),
    num_tickets INT,
    customer_name VARCHAR(100)
);
# 🚀 How to Run
Clone the repository:

bash
git clone https://github.com/<your-username>/Movie-Booking-System.git
Open the project folder and install required packages (if not already installed):

bash
pip install mysql-connector-python
Make sure your MySQL server is running and the credentials are correct in backend.py.

Run the main file:

bash
python movie_booking_gui.py

# 📷 Screenshots
![Screenshot 2025-04-30 132912](https://github.com/user-attachments/assets/8ee5f24c-eb44-4f28-b441-2b95703744d6)
![Screenshot 2025-04-30 132945](https://github.com/user-attachments/assets/9787083e-f0b1-4621-a5ba-350d461f7182)
![Screenshot 2025-04-30 133206](https://github.com/user-attachments/assets/dd3bd988-3066-4904-96b6-4ba4fba63e1d)
![Screenshot 2025-04-30 133259](https://github.com/user-attachments/assets/8c679ab9-dd64-467c-b3af-4e0c1242bbcf)


👤 Author
Suryansh Agrawal

📄 License
This project is open-source and available under the MIT License.
