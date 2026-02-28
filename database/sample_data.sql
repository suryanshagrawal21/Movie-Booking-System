-- Sample Data for Movie Booking System 2.0
USE movie_booking;

-- Note: Users table is seeded programmatically via setup_v2.py to ensure passwords are hashed with bcrypt.
-- Do not insert raw text passwords here.

-- Insert Sample Theaters
INSERT INTO theaters (name, location, total_capacity) VALUES
('PVR Cinemas', 'VR Mall, Chennai', 200),
('INOX', 'City Center, Mumbai', 150),
('Cinepolis', 'DLF Cyber Hub, Gurgaon', 180);

-- Insert Sample Movies
INSERT INTO movies (title, description, release_date, director, cast, budget, duration_minutes, rating, poster_path) VALUES
('Inception', 'A thief who steals corporate secrets through the use of dream-sharing technology.', '2010-07-16', 'Christopher Nolan', 'Leonardo DiCaprio, Joseph Gordon-Levitt', 160000000.00, 148, 8.8, NULL),
('Interstellar', 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity\'s survival.', '2014-11-07', 'Christopher Nolan', 'Matthew McConaughey, Anne Hathaway', 165000000.00, 169, 8.6, NULL),
('The Dark Knight', 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham.', '2008-07-18', 'Christopher Nolan', 'Christian Bale, Heath Ledger', 185000000.00, 152, 9.0, NULL);

-- Insert Sample Shows
-- These assume movie IDs 1, 2, 3 and theater IDs 1, 2, 3 exist from the above inserts.
INSERT INTO shows (movie_id, theater_id, show_time, base_price) VALUES
(1, 1, DATE_ADD(NOW(), INTERVAL 1 DAY), 15.00),
(2, 2, DATE_ADD(NOW(), INTERVAL 2 DAY), 12.50),
(3, 3, DATE_ADD(NOW(), INTERVAL 1 DAY), 18.00);

-- Insert Sample Seats for Theater 1
INSERT INTO seats (theater_id, row_name, seat_number, is_premium) VALUES
(1, 'A', 1, FALSE), (1, 'A', 2, FALSE), (1, 'A', 3, FALSE),
(1, 'A', 4, FALSE), (1, 'A', 5, FALSE), (1, 'B', 1, TRUE),
(1, 'B', 2, TRUE), (1, 'B', 3, TRUE), (1, 'B', 4, TRUE),
(1, 'B', 5, TRUE);
