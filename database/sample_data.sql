-- Sample Data for Movie Booking System
USE movie_booking;

-- Insert Sample Movies
INSERT INTO movies (movie_id, movie_name, release_date, director, cast, budget, duration, rating) VALUES
('M001', 'Inception', '2010-07-16', 'Christopher Nolan', 'Leonardo DiCaprio, Joseph Gordon-Levitt', 160000000, 2.48, 8.8),
('M002', 'The Dark Knight', '2008-07-18', 'Christopher Nolan', 'Christian Bale, Heath Ledger', 185000000, 2.32, 9.0),
('M003', 'Interstellar', '2014-11-07', 'Christopher Nolan', 'Matthew McConaughey, Anne Hathaway', 165000000, 2.49, 8.6),
('M004', 'Parasite', '2019-05-30', 'Bong Joon-ho', 'Song Kang-ho, Lee Sun-kyun', 11400000, 2.12, 8.6),
('M005', 'Avengers: Endgame', '2019-04-26', 'Anthony Russo', 'Robert Downey Jr., Chris Evans', 356000000, 3.01, 8.4);

-- Insert Sample Bookings
INSERT INTO bookings (movie_name, num_tickets, customer_name) VALUES
('Inception', 2, 'Alice Smith'),
('The Dark Knight', 1, 'Bob Jones'),
('Interstellar', 4, 'Charlie Brown');
