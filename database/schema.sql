-- Normalized Database Schema for Movie Booking System 2.0

CREATE DATABASE IF NOT EXISTS movie_booking;
USE movie_booking;

-- Disable foreign key checks for clean teardown during development
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS booking_seats;
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS seats;
DROP TABLE IF EXISTS shows;
DROP TABLE IF EXISTS theaters;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS users;
SET FOREIGN_KEY_CHECKS = 1;

-- 1. Users Table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Movies Table
CREATE TABLE movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    release_date DATE,
    director VARCHAR(100),
    cast TEXT,
    budget DECIMAL(15, 2),
    duration_minutes INT, -- Duration in minutes is more standard
    rating DECIMAL(3, 1),
    poster_path VARCHAR(255) -- Path to movie poster image
);

-- 3. Theaters Table
CREATE TABLE theaters (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(255),
    total_capacity INT NOT NULL
);

-- 4. Shows Table (Mapping Movies to Theaters and Time)
CREATE TABLE shows (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT NOT NULL,
    theater_id INT NOT NULL,
    show_time DATETIME NOT NULL,
    base_price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE,
    FOREIGN KEY (theater_id) REFERENCES theaters(id) ON DELETE CASCADE
);

-- 5. Seats Table
CREATE TABLE seats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    theater_id INT NOT NULL,
    seat_number INT NOT NULL,
    row_name CHAR(1) NOT NULL,
    is_premium BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (theater_id) REFERENCES theaters(id) ON DELETE CASCADE,
    UNIQUE(theater_id, row_name, seat_number)
);

-- 6. Bookings Table
CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    show_id INT NOT NULL,
    total_tickets INT NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    booking_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (show_id) REFERENCES shows(id) ON DELETE CASCADE
);

-- 7. Booking Seats Table (Specific seats for each booking)
CREATE TABLE booking_seats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    seat_id INT NOT NULL,
    FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE,
    FOREIGN KEY (seat_id) REFERENCES seats(id) ON DELETE CASCADE,
    UNIQUE(booking_id, seat_id)
);
