from pydantic import BaseModel
from datetime import datetime


class AirportOut(BaseModel):
    id: int
    code: str
    city: str
    name: str

    class Config:
        from_attributes = True


class FlightOut(BaseModel):
    id: int
    flight_number: str
    origin: AirportOut
    destination: AirportOut
    departure_time: datetime
    arrival_time: datetime
    price: float
    available_seats: int = 0

    class Config:
        from_attributes = True