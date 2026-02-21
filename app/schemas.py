from pydantic import BaseModel
from datetime import datetime

class MovieCreate(BaseModel):
    title: str
    genre: str


class ShowCreate(BaseModel):
    movie_id: int
    start_time: datetime
    end_time: datetime

class SeatCreate(BaseModel):
    show_id: int
    seat_number: int


class BookingCreate(BaseModel):
    user_name: str
    seat_id: int

class UserCreate(BaseModel):
    username: str
    password: str

class LoginSchema(BaseModel):
    username: str
    password: str