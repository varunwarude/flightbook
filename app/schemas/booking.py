from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BookingCreate(BaseModel):
    flight_id: int
    seat_id: int
    passenger_name: str
    passenger_age: Optional[int] = None


class BookingOut(BaseModel):
    id: int
    booking_reference: str
    flight_id: int
    seat_id: int
    passenger_name: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True