# Flightbook ✈️

A full-stack flight booking platform built with FastAPI, pandas, and scikit-learn. Supports user authentication, flight search, seat selection, booking management, booking analytics, and ML-based price prediction.

## Features

- JWT-based user authentication (register/login)
- Flight search by origin, destination, and date
- Real-time seat availability with visual seat map
- Booking creation with double-booking prevention
- Booking history and cancellation
- **Booking analytics** — revenue, popular routes, seat class breakdown, seat occupancy (pandas)
- **Visual charts** — bookings-per-route and occupancy-rate charts rendered server-side (matplotlib)
- **ML price prediction** — Random Forest model predicts flight price from route, day of week, and days-until-departure (scikit-learn)
- Responsive frontend built with vanilla HTML/CSS/JS

## Tech Stack

**Backend:** Python, FastAPI, SQLAlchemy, SQLite, Pydantic, JWT (python-jose), bcrypt password hashing

**Data/ML:** pandas, matplotlib, scikit-learn (Random Forest Regressor), joblib

**Frontend:** HTML, CSS, JavaScript (Fetch API)

## Project Structure

flightbook/
├── app/
│ ├── models/ # SQLAlchemy database models
│ ├── schemas/ # Pydantic request/response schemas
│ ├── routers/ # API endpoints (auth, flights, bookings, analytics, predict)
│ ├── ml/ # Model training script + saved model
│ ├── auth.py # JWT + password hashing logic
│ ├── database.py # DB connection setup
│ └── main.py # FastAPI app entry point
├── frontend/
│ └── index.html # Single-page frontend
├── seed.py # Sample data generator (112 flights across 8 routes)
└── requirements.txt

## Setup

1. Clone the repo and navigate into it
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\Activate.ps1` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. Install dependencies: `pip install -r requirements.txt`
5. Seed sample data: `python seed.py`
6. Train the ML model: `python app/ml/train_model.py`
7. Start the server: `uvicorn app.main:app --reload`
8. Open `frontend/index.html` in your browser
9. API docs available at `http://127.0.0.1:8000/docs`

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
| GET | `/analytics/summary` | Booking stats: revenue, popular routes, seat class split |
| GET | `/analytics/occupancy` | Seat occupancy rate per flight |
| GET | `/analytics/chart/routes` | Bar chart image: bookings per route |
| GET | `/analytics/chart/occupancy` | Bar chart image: occupancy rate per flight |
| POST | `/predict/price` | ML-predicted flight price for a given route/date |

## Machine Learning

`app/ml/train_model.py` trains a Random Forest Regressor on flight data (route, day of week, departure hour, days until departure) to predict ticket price. Achieves **R² ≈ 0.93** and **MAE ≈ ₹288** on held-out test data. The trained model is served via `/predict/price`.

## Author

Varun Warude — [GitHub](https://github.com/varunwarude) · [LinkedIn](https://linkedin.com/in/varun-warude-a71952359)