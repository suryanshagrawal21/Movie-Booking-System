# Interview Preparation Guide: Movie Booking System

Use this guide to explain your project effectively during technical interviews.

## 1. The 2-Minute Pitch
"I built a professional-grade **Movie Booking System** using Python's **CustomTkinter** for the frontend and **MySQL** for data persistence. The project follows a clean **MVC (Model-View-Controller) architecture**, ensuring a strict separation between UI logic, business rules, and database operations. Key features include role-based access control, a dynamic seat selection system with real-time availability checks, and automatic ticket generation in PDF format. I also implemented centralized logging and environment-based configuration to mimic industry-standard software development practices."

## 2. Technical Challenges & Solutions

### Challenge 1: Concurrent Seat Selection
**Problem**: Two users trying to book the same seat at the exact same time.
**Solution**: I implemented a **transactional booking process** at the database level. Before committing a booking, the system performs an atomic check to ensure the selected seat ID isn't already linked to the specific show in the `booking_seats` table. If a conflict is detected, the transaction rolls back, and the user receives a graceful error message.

### Challenge 2: Dynamic UI for Seat Mapping
**Problem**: Representing a theater's seating layout dynamically based on database records.
**Solution**: I created a `SeatSelectionView` that groups seats by `row_name` and `seat_number`. It uses a grid layout in CustomTkinter that color-codes buttons (Green: Available, Red: Occupied, Orange: Selected) by joining the `seats` table with the `booking_seats` table for the specific `show_id`.

## 3. Common Interview Questions

### Q: Why did you choose MySQL over SQLite?
**A**: While SQLite is simpler, MySQL allows for better concurrency handling and is more representative of real-world production environments where the database might reside on a separate server. It also allowed me to practice with more complex constraints and transactional logic.

### Q: How would you scale this to handle millions of users?
**A**: 
1. **Caching**: Use Redis to cache movie listings and seat availability to reduce database load.
2. **Database Sharding**: Partition the database by region or theater to distribute traffic.
3. **Microservices**: Break the system into separate services for Auth, Booking, and Payment.
4. **Load Balancers**: Deploy multiple instances of the backend behind a load balancer.

## 4. Architecture Explanation
- **Models**: Responsible for all SQL interactions (PEP 249 compliant).
- **Controllers**: Act as the brain, processing business logic and orchestrating between Models and Views.
- **Views**: Purely decorative and interactive, built with CustomTkinter for a modern "Dark Mode" aesthetic.
- **Utils**: Utility layer for cross-cutting concerns like PDF generation and logging.
