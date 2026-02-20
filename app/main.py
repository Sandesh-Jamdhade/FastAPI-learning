from fastapi import FastAPI
from app.routes import user_routes

app = FastAPI()
Students={
    1:{
        "name":"Sandesh",
        "age":21,
        "Degree":"MCA"
    }
}

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/get-student/{student_id}")
def get_student(student_id:int):
    return Students[student_id]

