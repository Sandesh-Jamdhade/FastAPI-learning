from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Seat

router = APIRouter(prefix="/seats", tags=["Seats"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Create seats
@router.post("/")
def create_seat(seat_number: str, db: Session = Depends(get_db)):

    existing_seat = db.query(Seat).filter(Seat.seat_number == seat_number).first()

    if existing_seat:
        raise HTTPException(status_code=400, detail="Seat already exists")

    seat = Seat(seat_number=seat_number)
    db.add(seat)
    db.commit()
    db.refresh(seat)

    return seat

@router.get("/")
def list_seats(db: Session = Depends(get_db)):
    return db.query(Seat).all()