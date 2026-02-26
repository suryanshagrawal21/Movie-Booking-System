# 🎬 Movie Booking System

A clean, Python-based desktop application for managing movie tickets and bookings. Built with **Tkinter** and **MySQL**.

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🚀 Features

*   **Movie Management**: Add, Update, Delete, and View movies.
*   **Booking System**: Book tickets for available movies with customer details.
*   **Search**: Filter movies by name.
*   **Modern UI**: Dark-themed interface with split-view layout.
*   **Data Persistence**: All data is stored securely in a MySQL database.

## 🛠️ Tech Stack

*   **Frontend**: Python Tkinter (using `ttk` for modern styling).
*   **Backend**: Python `mysql-connector`.
*   **Database**: MySQL.

## 📂 Project Structure

```
Movie-Booking-System/
├── src/
│   ├── main.py           # Application Entry Point
│   └── database.py       # Database Management Class
├── database/
│   ├── setup.py          # Database Initialization Script
│   ├── schema.sql        # Database Table Definitions
│   └── sample_data.sql   # Dummy Data for Testing
├── assets/               # Images and Screenshots
├── requirements.txt      # Python Dependencies
└── README.md             # Project Documentation
```

## 🗄️ Database Schema

The project uses a simple relational database structure:

### `movies` Table
Stores movie details.
-   `id`: Primary Key
-   `movie_id`: Unique Identifier (e.g., M001)
-   `movie_name`: Title
-   `release_date`, `director`, `cast`, `budget`, `duration`, `rating`

### `bookings` Table
Stores ticket booking records.
-   `id`: Primary Key
-   `movie_name`: Foreign Key reference (conceptual)
-   `num_tickets`: Count of tickets
-   `customer_name`: Name of the booker
-   `booking_time`: Timestamp

## 🚀 Future Improvements

*   **User Authentication**: Add Admin/User login.
*   **Seat Selection**: Visual seat map for booking.
*   **Payment Gateway**: Dummy payment processing.
*   **Email Notifications**: Send booking confirmation emails.
*   **Web Version**: Port frontend to Flask/Django.

## ⚙️ Installation & Setup

### Prerequisites
1.  **Python 3.x** installed.
│   ├── models/             # Data access layer (MySQL interactions)
│   ├── views/              # UI components (CustomTkinter)
│   ├── controllers/        # Business logic and services
│   ├── utils/              # Hashing, PDF generation, etc.
│   └── assets/             # Icons and images
├── tickets/                # Generated PDF tickets
├── tests/                  # Unit tests
├── run.py                  # Main application entry point
└── requirements.txt        # Project dependencies
```

## 🛠️ Installation & Setup

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/suryanshagrawal21/Movie-Booking-System.git
    cd Movie-Booking-System
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```


## ▶️ How to Run

Start the application:
```bash
python src/main.py
```

## 📸 Screenshots

![Dashboard Preview](assets/dashboard_preview.png)
*Main Dashboard showing Movie Management and Booking Interface*

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.
