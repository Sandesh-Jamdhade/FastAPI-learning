from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Show
from ..schemas import ShowCreate

router = APIRouter(prefix="/shows", tags=["Shows"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_show(show: ShowCreate, db: Session = Depends(get_db)):
    db_show = Show(**show.dict())
    db.add(db_show)
    db.commit()
    return db_show


@router.get("/")
def list_shows(db: Session = Depends(get_db)):
    return db.query(Show).all()

@router.delete("/shows/{show_id}")
def delete_show(show_id: int, db: Session = Depends(get_db)):

    show = db.query(Show).filter(Show.id == show_id).first()

    if not show:
        raise HTTPException(404, "Show not found")

    db.delete(show)
    db.commit()

    return {"message": "Show deleted"}