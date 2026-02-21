from pydantic import BaseModel

class MovieCreate(BaseModel):
    title: str
    genre: str


class ShowCreate(BaseModel):
    movie_id: int
    show_time: str


class SeatCreate(BaseModel):
    show_id: int
    seat_number: int


class BookingCreate(BaseModel):
    user_name: str
    seat_id: int