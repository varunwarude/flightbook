import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.seat import Seat
from app.models.booking import Booking
from app.schemas.booking import BookingCreate, BookingOut
from app.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("", response_model=BookingOut)
def create_booking(
    booking_in: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    seat = db.query(Seat).filter(
        Seat.id == booking_in.seat_id, Seat.flight_id == booking_in.flight_id
    ).with_for_update().first()

    if not seat:
        raise HTTPException(status_code=404, detail="Seat not found for this flight")
    if seat.is_booked:
        raise HTTPException(status_code=400, detail="Seat already booked")

    seat.is_booked = True

    booking = Booking(
        booking_reference=str(uuid.uuid4())[:8].upper(),
        user_id=current_user.id,
        flight_id=booking_in.flight_id,
        seat_id=booking_in.seat_id,
        passenger_name=booking_in.passenger_name,
        passenger_age=booking_in.passenger_age,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


@router.get("/my", response_model=list[BookingOut])
def my_bookings(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Booking).filter(Booking.user_id == current_user.id).all()


@router.post("/{booking_id}/cancel", response_model=BookingOut)
def cancel_booking(booking_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    booking = db.query(Booking).filter(Booking.id == booking_id, Booking.user_id == current_user.id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.status == "cancelled":
        raise HTTPException(status_code=400, detail="Booking already cancelled")

    booking.status = "cancelled"
    seat = db.query(Seat).filter(Seat.id == booking.seat_id).first()
    if seat:
        seat.is_booked = False

    db.commit()
    db.refresh(booking)
    return booking