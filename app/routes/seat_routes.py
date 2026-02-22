from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Seat
from ..redis_client import r
from ..schemas import SeatCreate, SeatLock
from ..auth_dependency import get_current_user

router = APIRouter(prefix="/seats", tags=["Seats"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/lock")
def lock_seat(data: SeatLock, user = Depends(get_current_user)):

    key = f"seat_lock:{data.show_id}:{data.seat_id}"

    if r.exists(key):
        raise HTTPException(status_code=400, detail="Seat already locked")

    r.setex(key, 120, user)

    return {"message": f"Seat locked by {user}"}


@router.post("/")
def create_seat(data: SeatCreate, db: Session = Depends(get_db)):

    existing_seat = db.query(Seat).filter(
        Seat.seat_number == data.seat_number
    ).first()

    if existing_seat:
        raise HTTPException(status_code=400, detail="Seat already exists")

    seat = Seat(seat_number=data.seat_number)
    db.add(seat)
    db.commit()
    db.refresh(seat)

    return seat


@router.get("/")
def list_seats(db: Session = Depends(get_db)):
    return db.query(Seat).all()