from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Seat, Booking
from ..schemas import BookingCreate
from ..auth_dependency import get_current_user
from ..redis_client import r

router = APIRouter(prefix="/booking", tags=["Booking"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def book_seat(
    data: BookingCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):

    key = f"seat_lock:{data.show_id}:{data.seat_id}"

    locked_by = r.get(key)

    if not locked_by:
        raise HTTPException(status_code=400, detail="Seat not locked")

    if locked_by != user:
        raise HTTPException(status_code=400, detail="Seat locked by another user")

    seat = db.query(Seat).filter(Seat.id == data.seat_id).first()

    if not seat:
        raise HTTPException(status_code=404, detail="Seat not found")

    if seat.is_booked:
        raise HTTPException(status_code=400, detail="Seat already booked")

    seat.is_booked = True

    booking = Booking(
        user_name=user,
        seat_id=data.seat_id
    )

    db.add(booking)
    db.commit()

    r.delete(key)

    return {"message": f"Seat booked successfully by {user}"}

@router.delete("/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db)):

    booking = db.query(Booking).filter(Booking.id == booking_id).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    seat = db.query(Seat).filter(Seat.id == booking.seat_id).first()

    if seat:
        seat.is_booked = False

    db.delete(booking)
    db.commit()

    return {"message": "Booking cancelled and seat released"}