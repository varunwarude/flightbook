import random
from datetime import datetime, timedelta
from app.database import SessionLocal, Base, engine
from app.models.flight import Airport, Flight
from app.models.seat import Seat

Base.metadata.create_all(bind=engine)
db = SessionLocal()

random.seed(42)

airports_data = [
    ("PNQ", "Pune", "Pune Airport"),
    ("BOM", "Mumbai", "Chhatrapati Shivaji Maharaj International"),
    ("DEL", "Delhi", "Indira Gandhi International"),
    ("BLR", "Bangalore", "Kempegowda International"),
]

airports = {}
for code, city, name in airports_data:
    existing = db.query(Airport).filter(Airport.code == code).first()
    if not existing:
        existing = Airport(code=code, city=city, name=name)
        db.add(existing)
        db.commit()
        db.refresh(existing)
    airports[code] = existing

routes = [
    ("PNQ", "DEL", 2.0, 6000),
    ("PNQ", "BOM", 1.0, 3000),
    ("PNQ", "BLR", 1.5, 4000),
    ("BOM", "DEL", 2.0, 5500),
    ("BOM", "BLR", 1.5, 4200),
    ("DEL", "BLR", 2.5, 6800),
    ("DEL", "BOM", 2.0, 5800),
    ("BLR", "PNQ", 1.5, 4100),
]

flight_counter = 1
for origin, dest, base_hours, base_price in routes:
    for day_offset in range(1, 15):
        number = f"FL{flight_counter:04d}"
        flight_counter += 1

        existing = db.query(Flight).filter(Flight.flight_number == number).first()
        if existing:
            continue

        dep_hour = random.choice([6, 9, 12, 15, 18, 21])
        dep = datetime.now().replace(hour=dep_hour, minute=0, second=0, microsecond=0) + timedelta(days=day_offset)
        arr = dep + timedelta(hours=base_hours)

        urgency_factor = max(0, (10 - day_offset) * 50)
        price = round(base_price + urgency_factor + random.randint(-300, 500), -1)

        f = Flight(
            flight_number=number,
            origin_id=airports[origin].id,
            destination_id=airports[dest].id,
            departure_time=dep,
            arrival_time=arr,
            price=price,
            total_seats=30,
        )
        db.add(f)
        db.commit()
        db.refresh(f)

        for row in range(1, 6):
            for col in "ABCDEF":
                seat_class = "business" if row <= 1 else "economy"
                db.add(Seat(flight_id=f.id, seat_number=f"{row}{col}", seat_class=seat_class))
        db.commit()

print("Seed complete.")
db.close()