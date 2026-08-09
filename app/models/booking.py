from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    booking_reference = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    flight_id = Column(Integer, ForeignKey("flights.id"), nullable=False)
    seat_id = Column(Integer, ForeignKey("seats.id"), nullable=False)
    passenger_name = Column(String, nullable=False)
    passenger_age = Column(Integer, nullable=True)
    status = Column(String, default="confirmed")  # confirmed, cancelled
    created_at = Column(DateTime, server_default=func.now())

    flight = relationship("Flight")
    seat = relationship("Seat")