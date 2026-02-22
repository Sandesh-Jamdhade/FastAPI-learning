from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Movie
from ..schemas import MovieCreate
from ..redis_client import r
import json

router = APIRouter(prefix="/movies", tags=["Movies"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_movies(db: Session = Depends(get_db)):

    cached = r.get("movies_list")

    if cached:
        return json.loads(cached)

    movies = db.query(Movie).all()

    data = [{"id": m.id, "name": m.name} for m in movies]

    r.setex("movies_list", 60, json.dumps(data))  

    return data

@router.post("/")
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):

    existing_movie = db.query(Movie).filter(Movie.name == movie.name).first()

    if existing_movie:
        raise HTTPException(status_code=400, detail="Movie already exists")

    db_movie = Movie(name=movie.name)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)

    r.delete("movies_list")

    return db_movie


@router.delete("/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):

    movie = db.query(Movie).filter(Movie.id == movie_id).first()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    db.delete(movie)
    db.commit()

    r.delete("movies_list")

    return {"message": "Movie deleted successfully"}