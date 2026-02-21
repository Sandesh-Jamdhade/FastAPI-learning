from fastapi import APIRouter, Depends
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