# Flightbook ✈️

A full-stack flight booking platform built with FastAPI and vanilla JavaScript. Supports user authentication, flight search, seat selection, and booking management with race-condition-safe seat locking.

## Features

- JWT-based user authentication (register/login)
- Flight search by origin, destination, and date
- Real-time seat availability with visual seat map
- Booking creation with double-booking prevention
- Booking history and cancellation
- Responsive frontend built with vanilla HTML/CSS/JS

## Tech Stack

**Backend:** Python, FastAPI, SQLAlchemy, SQLite, Pydantic, JWT (python-jose), bcrypt password hashing

**Frontend:** HTML, CSS, JavaScript (Fetch API)

## Project Structure

flightbook/
├── app/
│ ├── models/ # SQLAlchemy database models
│ ├── schemas/ # Pydantic request/response schemas
│ ├── routers/ # API endpoints (auth, flights, bookings)
│ ├── auth.py # JWT + password hashing logic
│ ├── database.py # DB connection setup
│ └── main.py # FastAPI app entry point
├── frontend/
│ └── index.html # Single-page frontend
├── seed.py # Sample data generator
└── requirements.txt

## Setup

1. Clone the repo and navigate into it
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\Activate.ps1` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. Install dependencies: `pip install -r requirements.txt`
5. Seed sample data: `python seed.py`
6. Start the server: `uvicorn app.main:app --reload`
7. Open `frontend/index.html` in your browser
8. API docs available at `http://127.0.0.1:8000/docs`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Create a new user |
| POST | `/auth/login` | Log in and receive a JWT token |
| GET | `/flights/search` | Search flights by origin/destination/date |
| GET | `/flights/{id}/seats` | View seat availability for a flight |
| POST | `/bookings` | Book a seat |
| GET | `/bookings/my` | View your bookings |
| POST | `/bookings/{id}/cancel` | Cancel a booking |

## Author

Varun Warude — [GitHub](https://github.com/varunwarude) · [LinkedIn](https://linkedin.com/in/varun-warude-a71952359)S