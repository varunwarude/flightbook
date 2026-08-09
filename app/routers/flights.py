from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional
from datetime import datetime

from app.database import get_db
from app.models.flight import Flight, Airport
from app.models.seat import Seat
from app.schemas.flight import FlightOut

router = APIRouter(prefix="/flights", tags=["flights"])


@router.get("/search", response_model=list[FlightOut])
def search_flights(
    origin: Optional[str] = None,
    destination: Optional[str] = None,
    date: Optional[str] = None,  # format: YYYY-MM-DD
    db: Session = Depends(get_db),
):
    query = db.query(Flight)

    if origin:
        origin_airport = db.query(Airport).filter(Airport.code == origin.upper()).first()
        if origin_airport:
            query = query.filter(Flight.origin_id == origin_airport.id)

    if destination:
        dest_airport = db.query(Airport).filter(Airport.code == destination.upper()).first()
        if dest_airport:
            query = query.filter(Flight.destination_id == dest_airport.id)

    if date:
        day_start = datetime.strptime(date, "%Y-%m-%d")
        day_end = day_start.replace(hour=23, minute=59, second=59)
        query = query.filter(and_(Flight.departure_time >= day_start, Flight.departure_time <= day_end))

    flights = query.all()

    results = []
    for f in flights:
        available = db.query(Seat).filter(Seat.flight_id == f.id, Seat.is_booked == False).count()
        item = FlightOut.model_validate(f)
        item.available_seats = available
        results.append(item)

    return results


@router.get("/{flight_id}/seats")
def get_flight_seats(flight_id: int, db: Session = Depends(get_db)):
    seats = db.query(Seat).filter(Seat.flight_id == flight_id).all()
    return [
        {"id": s.id, "seat_number": s.seat_number, "seat_class": s.seat_class, "is_booked": s.is_booked}
        for s in seats
    ]