from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Seat(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True, index=True)
    flight_id = Column(Integer, ForeignKey("flights.id"), nullable=False)
    seat_number = Column(String, nullable=False)  # e.g. "14A"
    seat_class = Column(String, default="economy")  # economy, business
    is_booked = Column(Boolean, default=False)

    flight = relationship("Flight", back_populates="seats")