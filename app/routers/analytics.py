import pandas as pd
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import io
from fastapi.responses import StreamingResponse

from app.database import get_db

router = APIRouter(prefix="/analytics", tags=["analytics"])


def load_bookings_df(db: Session) -> pd.DataFrame:
    query = text("""
        SELECT
            b.id AS booking_id,
            b.status,
            b.created_at,
            f.flight_number,
            f.price,
            f.departure_time,
            oa.city AS origin_city,
            oa.code AS origin_code,
            da.city AS destination_city,
            da.code AS destination_code,
            s.seat_class
        FROM bookings b
        JOIN flights f ON b.flight_id = f.id
        JOIN airports oa ON f.origin_id = oa.id
        JOIN airports da ON f.destination_id = da.id
        JOIN seats s ON b.seat_id = s.id
    """)
    result = db.execute(query)
    rows = result.fetchall()
    columns = result.keys()
    return pd.DataFrame(rows, columns=columns)


@router.get("/summary")
def analytics_summary(db: Session = Depends(get_db)):
    df = load_bookings_df(db)

    if df.empty:
        return {
            "total_bookings": 0,
            "confirmed_bookings": 0,
            "cancelled_bookings": 0,
            "total_revenue": 0,
            "routes": [],
            "seat_class_breakdown": {},
        }

    df["route"] = df["origin_code"] + " → " + df["destination_code"]
    confirmed = df[df["status"] == "confirmed"]

    route_counts = (
        confirmed.groupby("route")
        .size()
        .sort_values(ascending=False)
        .reset_index(name="bookings")
        .to_dict(orient="records")
    )

    seat_class_breakdown = (
        confirmed["seat_class"].value_counts().to_dict()
    )

    return {
        "total_bookings": int(len(df)),
        "confirmed_bookings": int(len(confirmed)),
        "cancelled_bookings": int(len(df[df["status"] == "cancelled"])),
        "total_revenue": float(confirmed["price"].sum()),
        "routes": route_counts,
        "seat_class_breakdown": seat_class_breakdown,
    }


@router.get("/occupancy")
def seat_occupancy(db: Session = Depends(get_db)):
    query = text("""
        SELECT
            f.id AS flight_id,
            f.flight_number,
            f.total_seats,
            SUM(CASE WHEN s.is_booked = 1 THEN 1 ELSE 0 END) AS booked_seats
        FROM flights f
        LEFT JOIN seats s ON s.flight_id = f.id
        GROUP BY f.id
    """)
    result = db.execute(query)
    rows = result.fetchall()
    columns = result.keys()
    df = pd.DataFrame(rows, columns=columns)

    if df.empty:
        return []

    df["occupancy_rate"] = (df["booked_seats"] / df["total_seats"] * 100).round(1)
    return df.to_dict(orient="records")


@router.get("/chart/routes")
def chart_popular_routes(db: Session = Depends(get_db)):
    df = load_bookings_df(db)

    if df.empty:
        raise HTTPException(status_code=404, detail="No booking data available yet")

    df["route"] = df["origin_code"] + " → " + df["destination_code"]
    confirmed = df[df["status"] == "confirmed"]
    route_counts = confirmed["route"].value_counts()

    fig, ax = plt.subplots(figsize=(8, 5))
    route_counts.plot(kind="bar", ax=ax, color="#38bdf8")
    ax.set_title("Bookings per Route")
    ax.set_xlabel("Route")
    ax.set_ylabel("Number of Bookings")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")


@router.get("/chart/occupancy")
def chart_occupancy(db: Session = Depends(get_db)):
    query = text("""
        SELECT
            f.flight_number,
            f.total_seats,
            SUM(CASE WHEN s.is_booked = 1 THEN 1 ELSE 0 END) AS booked_seats
        FROM flights f
        LEFT JOIN seats s ON s.flight_id = f.id
        GROUP BY f.id
        LIMIT 15
    """)
    result = db.execute(query)
    rows = result.fetchall()
    columns = result.keys()
    df = pd.DataFrame(rows, columns=columns)

    if df.empty:
        raise HTTPException(status_code=404, detail="No flight data available")

    df["occupancy_rate"] = (df["booked_seats"] / df["total_seats"] * 100).round(1)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(df["flight_number"], df["occupancy_rate"], color="#4ade80")
    ax.set_title("Seat Occupancy Rate by Flight (first 15)")
    ax.set_xlabel("Flight Number")
    ax.set_ylabel("Occupancy %")
    ax.set_ylim(0, 100)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")