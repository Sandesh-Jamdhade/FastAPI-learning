from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Seat, Booking
from ..schemas import BookingCreate

router = APIRouter(prefix="/booking", tags=["Booking"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def book_seat(data: BookingCreate, db: Session = Depends(get_db)):

    seat = db.query(Seat).filter(Seat.id == data.seat_id).first()

    if not seat:
        raise HTTPException(404, "Seat not found")

    if seat.is_booked:
        raise HTTPException(400, "Seat already booked")

    seat.is_booked = True

    booking = Booking(user_name=data.user_name, seat_id=data.seat_id)
    db.add(booking)
    db.commit()

    return {"message": "Seat booked successfully"}