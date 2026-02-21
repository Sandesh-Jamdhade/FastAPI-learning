from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, UniqueConstraint, DateTime
from .database import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    genre = Column(String)

    __table_args__ = (
        UniqueConstraint("title", name="unique_movie_title"),
    )

class Show(Base):
    __tablename__ = "shows"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)


class Seat(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True, index=True)
    seat_number = Column(String, unique=True, index=True) 
    is_booked = Column(Boolean, default=False)


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String)
    seat_id = Column(Integer, ForeignKey("seats.id"))

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)