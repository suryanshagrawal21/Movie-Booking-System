-- Database Schema for Movie Booking System

CREATE DATABASE IF NOT EXISTS movie_booking;
USE movie_booking;

-- Movies Table
CREATE TABLE IF NOT EXISTS movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id VARCHAR(20) UNIQUE NOT NULL,
    movie_name VARCHAR(100) NOT NULL,
    release_date DATE,
    director VARCHAR(100),
    cast TEXT,
    budget DECIMAL(15, 2), -- Increased precision
    duration DECIMAL(4, 2), -- In hours (e.g., 2.5)
    rating DECIMAL(3, 1)    -- e.g., 8.5
);

-- Bookings Table
CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_name VARCHAR(255) NOT NULL,
    num_tickets INT NOT NULL,
    customer_name VARCHAR(255) NOT NULL,
    booking_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
