import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
from datetime import datetime
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from app.database import SessionLocal
from sqlalchemy import text


def load_training_data():
    db = SessionLocal()
    query = text("""
        SELECT
            f.price,
            f.departure_time,
            oa.code AS origin_code,
            da.code AS destination_code
        FROM flights f
        JOIN airports oa ON f.origin_id = oa.id
        JOIN airports da ON f.destination_id = da.id
    """)
    result = db.execute(query)
    rows = result.fetchall()
    columns = result.keys()
    db.close()
    return pd.DataFrame(rows, columns=columns)


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["departure_time"] = pd.to_datetime(df["departure_time"])
    df["days_until_departure"] = (df["departure_time"] - datetime.now()).dt.days
    df["days_until_departure"] = df["days_until_departure"].clip(lower=0)
    df["departure_hour"] = df["departure_time"].dt.hour
    df["day_of_week"] = df["departure_time"].dt.dayofweek
    df["route"] = df["origin_code"] + "_" + df["destination_code"]
    return df


def train():
    print("Loading data from database...")
    df = load_training_data()
    print(f"Loaded {len(df)} flights.")

    df = build_features(df)

    features = ["route", "days_until_departure", "departure_hour", "day_of_week"]
    X = df[features]
    y = df["price"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    preprocessor = ColumnTransformer(
        transformers=[
            ("route_encoded", OneHotEncoder(handle_unknown="ignore"), ["route"]),
        ],
        remainder="passthrough",
    )

    model = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(n_estimators=200, random_state=42)),
    ])

    print("Training model...")
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Mean Absolute Error: ₹{mae:.2f}")
    print(f"R² Score: {r2:.3f}")

    model_path = os.path.join(os.path.dirname(__file__), "price_model.joblib")
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")


if __name__ == "__main__":
    train()