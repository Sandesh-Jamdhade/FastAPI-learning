from fastapi import FastAPI
from .database import Base, engine
from .routes import movie_routes, show_routes, booking_routes, seat_routes, user_routes
from .scheduler import start_scheduler

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Movie Booking API")

start_scheduler()

app.include_router(user_routes.router)
app.include_router(seat_routes.router)
app.include_router(movie_routes.router)
app.include_router(show_routes.router)
app.include_router(booking_routes.router)