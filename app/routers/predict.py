import os
import joblib
import pandas as pd
from datetime import datetime
from fastapi import APIRouter, HTTPException

from app.schemas.prediction import PricePredictionRequest, PricePredictionResponse

router = APIRouter(prefix="/predict", tags=["prediction"])

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "ml", "price_model.joblib")
_model = None


def get_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise HTTPException(status_code=503, detail="Model not trained yet. Run train_model.py first.")
        _model = joblib.load(MODEL_PATH)
    return _model


@router.post("/price", response_model=PricePredictionResponse)
def predict_price(req: PricePredictionRequest):
    model = get_model()

    try:
        dep_date = datetime.strptime(req.departure_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="departure_date must be in YYYY-MM-DD format")

    days_until = max(0, (dep_date - datetime.now()).days)
    route = f"{req.origin.upper()}_{req.destination.upper()}"

    X = pd.DataFrame([{
        "route": route,
        "days_until_departure": days_until,
        "departure_hour": req.departure_hour,
        "day_of_week": dep_date.weekday(),
    }])

    predicted_price = float(model.predict(X)[0])

    return PricePredictionResponse(
        predicted_price=round(predicted_price, 2),
        route=route,
        days_until_departure=days_until,
    )