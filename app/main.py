from fastapi import FastAPI
from app.routes import user_routes
from pydantic import BaseModel
from typing import Optional

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

#Fetching the Data of the user

@app.get("/get-student/{student_id}")
def get_student(student_id:int):
    return Students[student_id]

#Create New Student
class Student(BaseModel):
    name:str
    age:int
    Degree:str

@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in Students:
        return {"Error": "Already Exists"}

    Students[student_id] = student
    return {"message": "Student created"}




