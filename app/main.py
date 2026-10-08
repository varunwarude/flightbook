from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models import user, flight, seat, booking  # noqa: F401
from app.routers import auth, flights, bookings, analytics, predict


# Create database tables
Base.metadata.create_all(bind=engine)

# Seed initial demo data
try:
    from seed_data import seed_database
    seed_database()
except Exception as e:
    print(f"Database seeding skipped/failed: {e}")


app = FastAPI(title="Flightbook API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(flights.router)
app.include_router(bookings.router)
app.include_router(analytics.router)
app.include_router(predict.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
