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

## ⚙️ Installation & Setup

### Prerequisites
1.  **Python 3.x** installed.
2.  **MySQL Server** installed and running.

### Steps

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/suryanshagrawal21/Movie-Booking-System.git
    cd Movie-Booking-System
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Setup Database**
    Run the setup script to create the database and tables.
    ```bash
    python database/setup.py
    ```
    *   *Note: If your MySQL root password is not the default, the script will prompt you to enter it.*

## ▶️ How to Run

Start the application:
```bash
python src/main.py
```

## 📸 Screenshots

*(Add screenshots of your application here)*

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.
