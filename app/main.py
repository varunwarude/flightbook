from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.models import user, flight, seat, booking  # noqa: F401
from app.routers import auth, flights, bookings

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Flightbook API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(flights.router)
app.include_router(bookings.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}