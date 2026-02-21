from fastapi import FastAPI
from app.database import Base, engine 
from app.routes import movie_routes, show_routes, booking_routes, seat_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Movie Booking API")


app.include_router(seat_routes.router)
app.include_router(movie_routes.router)
app.include_router(show_routes.router)
app.include_router(booking_routes.router)


