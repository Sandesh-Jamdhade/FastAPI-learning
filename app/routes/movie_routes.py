from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Movie
from ..schemas import MovieCreate

router = APIRouter(prefix="/movies", tags=["Movies"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):

    existing_movie = db.query(Movie).filter(Movie.title == movie.title).first()

    if existing_movie:
        raise HTTPException(status_code=400, detail="Movie already exists")

    db_movie = Movie(**movie.dict())
    db.add(db_movie)
    db.commit()

    return db_movie


@router.get("/")
def list_movies(db: Session = Depends(get_db)):
    return db.query(Movie).all()

@router.delete("/movies/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):

    movie = db.query(Movie).filter(Movie.id == movie_id).first()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    db.delete(movie)
    db.commit()

    return {"message": "Movie deleted successfully"}