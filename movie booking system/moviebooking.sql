
CREATE DATABASE movie_booking;
USE movie_booking;
CREATE TABLE movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id VARCHAR(20) UNIQUE,
    movie_name VARCHAR(100),
    release_date DATE,
    director VARCHAR(100),
    cast TEXT,
    budget DECIMAL(10, 2),
    duration DECIMAL(4, 2),
    rating DECIMAL(2, 1)
);
CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_name VARCHAR(255),
    num_tickets INT,
    customer_name VARCHAR(255),
    booking_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


select* from movies;
select* from bookings;

