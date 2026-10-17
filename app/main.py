
from datetime import date
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Startup Booking API",
    description="An API for managing service bookings.",
    version="0.2.0",
)


class BookingCreate(BaseModel):
    customer_name: str = Field(min_length=2, max_length=100)
    service: str = Field(min_length=2, max_length=200)
    booking_date: date


class Booking(BookingCreate):
    id: str
    status: str = "pending"


bookings: dict[str, Booking] = {}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/bookings", status_code=201)
def create_booking(booking_data: BookingCreate):
    booking_id = str(uuid4())

    booking = Booking(
        id=booking_id,
        customer_name=booking_data.customer_name,
        service=booking_data.service,
        booking_date=booking_data.booking_date,
    )

    bookings[booking_id] = booking
    return booking


@app.get("/bookings")
def list_bookings():
    return list(bookings.values())


@app.get("/bookings/{booking_id}")
def get_booking(booking_id: str):
    booking = bookings.get(booking_id)

    if booking is None:
        raise HTTPException(
            status_code=404,
            detail="Booking not found",
        )

    return booking


