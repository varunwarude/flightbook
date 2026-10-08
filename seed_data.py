from datetime import datetime, timedelta

from app.database import SessionLocal, Base, engine
from app.models.flight import Airport, Flight
from app.models.seat import Seat


def seed_database():
    # Make sure tables exist
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # -------------------------------------------------
        # 1. Airports
        # -------------------------------------------------
        airports_data = [
            {
                "code": "PNQ",
                "city": "Pune",
                "name": "Pune International Airport",
            },
            {
                "code": "BOM",
                "city": "Mumbai",
                "name": "Chhatrapati Shivaji Maharaj International Airport",
            },
            {
                "code": "DEL",
                "city": "Delhi",
                "name": "Indira Gandhi International Airport",
            },
            {
                "code": "BLR",
                "city": "Bangalore",
                "name": "Kempegowda International Airport",
            },
            {
                "code": "HYD",
                "city": "Hyderabad",
                "name": "Rajiv Gandhi International Airport",
            },
        ]

        airports = {}

        for data in airports_data:
            airport = (
                db.query(Airport)
                .filter(Airport.code == data["code"])
                .first()
            )

            if not airport:
                airport = Airport(**data)
                db.add(airport)
                db.flush()

            airports[data["code"]] = airport

        # -------------------------------------------------
        # 2. Flights
        # -------------------------------------------------
        today = datetime.now()

        flights_data = [
            {
                "flight_number": "FB101",
                "origin": "PNQ",
                "destination": "BOM",
                "days": 7,
                "departure_hour": 8,
                "departure_minute": 30,
                "arrival_hour": 9,
                "arrival_minute": 45,
                "price": 3200,
            },
            {
                "flight_number": "FB102",
                "origin": "PNQ",
                "destination": "DEL",
                "days": 8,
                "departure_hour": 10,
                "departure_minute": 0,
                "arrival_hour": 12,
                "arrival_minute": 15,
                "price": 5800,
            },
            {
                "flight_number": "FB103",
                "origin": "PNQ",
                "destination": "BLR",
                "days": 9,
                "departure_hour": 14,
                "departure_minute": 30,
                "arrival_hour": 16,
                "arrival_minute": 10,
                "price": 4500,
            },
            {
                "flight_number": "FB104",
                "origin": "PNQ",
                "destination": "HYD",
                "days": 10,
                "departure_hour": 9,
                "departure_minute": 15,
                "arrival_hour": 10,
                "arrival_minute": 45,
                "price": 3900,
            },
            {
                "flight_number": "FB105",
                "origin": "BOM",
                "destination": "DEL",
                "days": 11,
                "departure_hour": 18,
                "departure_minute": 0,
                "arrival_hour": 20,
                "arrival_minute": 15,
                "price": 6200,
            },
            {
                "flight_number": "FB106",
                "origin": "BLR",
                "destination": "PNQ",
                "days": 12,
                "departure_hour": 11,
                "departure_minute": 30,
                "arrival_hour": 13,
                "arrival_minute": 0,
                "price": 4400,
            },
        ]

        for data in flights_data:
            existing_flight = (
                db.query(Flight)
                .filter(
                    Flight.flight_number == data["flight_number"]
                )
                .first()
            )

            if existing_flight:
                continue

            departure_date = today + timedelta(days=data["days"])

            departure_time = departure_date.replace(
                hour=data["departure_hour"],
                minute=data["departure_minute"],
                second=0,
                microsecond=0,
            )

            arrival_time = departure_date.replace(
                hour=data["arrival_hour"],
                minute=data["arrival_minute"],
                second=0,
                microsecond=0,
            )

            flight = Flight(
                flight_number=data["flight_number"],
                origin_id=airports[data["origin"]].id,
                destination_id=airports[data["destination"]].id,
                departure_time=departure_time,
                arrival_time=arrival_time,
                price=data["price"],
                total_seats=30,
            )

            db.add(flight)
            db.flush()

            # -------------------------------------------------
            # 3. Create seats
            # -------------------------------------------------
            for row in range(1, 7):
                for seat_letter in ["A", "B", "C", "D", "E"]:
                    seat = Seat(
                        flight_id=flight.id,
                        seat_number=f"{row}{seat_letter}",
                        seat_class="economy",
                        is_booked=False,
                    )
                    db.add(seat)

            # Add 5 business-class seats
            for seat_number in ["1F", "2F", "3F", "4F", "5F"]:
                seat = Seat(
                    flight_id=flight.id,
                    seat_number=seat_number,
                    seat_class="business",
                    is_booked=False,
                )
                db.add(seat)

        db.commit()

        print("Database seeded successfully!")
        print("Airports:", db.query(Airport).count())
        print("Flights:", db.query(Flight).count())
        print("Seats:", db.query(Seat).count())

    except Exception as e:
        db.rollback()
        print("Error while seeding database:")
        print(e)
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
