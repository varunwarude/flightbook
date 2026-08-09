from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Airport(Base):
    __tablename__ = "airports"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(3), unique=True, index=True, nullable=False)  # e.g. "PNQ"
    city = Column(String, nullable=False)
    name = Column(String, nullable=False)


class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String, unique=True, index=True, nullable=False)
    origin_id = Column(Integer, ForeignKey("airports.id"), nullable=False)
    destination_id = Column(Integer, ForeignKey("airports.id"), nullable=False)
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)
    total_seats = Column(Integer, default=180)

    origin = relationship("Airport", foreign_keys=[origin_id])
    destination = relationship("Airport", foreign_keys=[destination_id])
    seats = relationship("Seat", back_populates="flight")