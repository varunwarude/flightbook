from pydantic import BaseModel


class PricePredictionRequest(BaseModel):
    origin: str
    destination: str
    departure_date: str  # format: YYYY-MM-DD
    departure_hour: int = 12


class PricePredictionResponse(BaseModel):
    predicted_price: float
    route: str
    days_until_departure: int