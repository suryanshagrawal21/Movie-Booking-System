# Cinema Pro - Movie Booking System

This is a premium, startup-level implementation of a Movie Ticket Booking System built using Python, CustomTkinter, and MySQL. It's designed to simulate a real-world platform like BookMyShow or Netflix.

## 🚀 Key Features
* **Premium Dark Mode UI:** Modern aesthetics using CustomTkinter with glassmorphism effects, smooth animations, and a responsive grid layout.
* **Live Movie Data (TMDB API):** Real-time 'Now Playing' movies synced directly from The Movie Database (TMDB) with dynamic poster caching.
* **Interactive Seat Selection:** Visual theater layout with VIP premium seat markups, dynamic pricing, and disabled occupied seats.
* **Secure Authentication:** Passwords hashed with bcrypt, strict email/password validation, and automatic session timeouts (30 mins).
* **Booking Ecosystem:** Complete flow from selection to payment simulation gateway, ending with a dynamic digital PDF ticket generation (with fake barcode layout).

## 🛠️ Architecture Overview (MVC Pattern)
The codebase strictly adheres to the Model-View-Controller (MVC) architectural pattern:

```
src/
├── models/         # Database operations, abstractions, queries
├── views/          # UI components (CustomTkinter interfaces)
├── controllers/    # Business logic (Auth, Booking services)
├── services/       # External integrations (TMDB API)
└── utils/          # Helpers (Logging, PDF gen, Config management)
```

## 🔐 Security Enhancements
Security was prioritized for production readiness:
1. **Parameterized Queries:** Complete defense against SQL Injection attacks.
2. **Environment Variables (.env):** Sensitive database credentials and API keys are strictly kept out of source code.
3. **Bcrypt Hashing:** User passwords are encrypted before storage.
4. **Session Hardening:** 30-minute inactivity timeouts implemented globally to prevent session hijacking.
5. **Input Sanitation:** Regex-based validation on all input fields.

## ⚡ Scalability Considerations
* **Database Normalization:** 3NF design tracking Theaters, Shows, Seats, and Users independently.
* **Image Caching:** TMDB poster assets are cached locally (`src/assets/posters/`) to prevent rate limits and drop load times.
* **Transaction Safety:** MySQL atomic commits ensure a seat cannot be double-booked during concurrent requests.

## 👔 Interview Talking Points
1. *"I separated the TMDB integration into a specific Service Layer, so if the API changes, our core models remain unaffected."*
2. *"I implemented an initial health check on startup that uses an empty DB parameter to verify credentials before attempting to bind to the specific schema."*
3. *"I utilized ReportLab to dynamically build vector-based PDF tickets because it allowed me to overlay a dark-mode theme directly onto the printable document."*

## Running the Application
Ensure you have the latest packages installed and your `.env` configured inside the root directory.

```bash
pip install -r requirements.txt
python database/setup_v2.py  # Seed the database
python run.py                # Launch the app
```
