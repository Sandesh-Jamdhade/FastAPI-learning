from fastapi import FastAPI
from app.routes import user_routes

app = FastAPI()
@app.get("/")
async def root():
    return {"message": "API is running"}

app.include_router(user_routes.router)