from datetime import datetime, timedelta
from app.database import SessionLocal, Base, engine
from app.models.flight import Airport, Flight
from app.models.seat import Seat

Base.metadata.create_all(bind=engine)
db = SessionLocal()

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

flights_data = [
    ("6E101", "PNQ", "DEL", 2, 6500),
    ("6E202", "BOM", "BLR", 1.5, 4200),
    ("AI303", "DEL", "BOM", 2, 5800),
]

for number, origin, dest, hours, price in flights_data:
    existing = db.query(Flight).filter(Flight.flight_number == number).first()
    if existing:
        continue
    dep = datetime.now() + timedelta(days=3, hours=10)
    arr = dep + timedelta(hours=hours)
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