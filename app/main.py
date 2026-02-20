from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
students={
    1:{
        "name":"Sandesh",
        "age":21,
        "Degree":"MCA"
    }
}

#Fetching the Data of the user

@app.get("/get-student/{student_id}")
def get_student(student_id:int):
    return students[student_id]

#Create New Student
class Student(BaseModel):
    name:str
    age:int
    Degree:str

@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "Already Exists"}

    students[student_id] = student
    return {"message": "Student created"}

#Update Existing Student
class UpdateStudent(BaseModel):
    name:Optional[str]=None
    age:Optional[int]=None
    Degree:Optional[str]=None

@app.put("/update-student/{student_id}")
def update_student(student_id:int,student:UpdateStudent):
    if student_id not in students:
        return{"Data":"Not Exist"}
    if student.name!=None:
        students[student_id].name=student.name
    if student.age!=None:
        students[student_id].age=student.age
    if student.Degree!=None:
        students[student_id].Degree=student.Degree
    return students[student_id]

#Deleting Student
@app.delete("/delete-student/{student_id}")
def delete_student(student_id:int):
    if student_id not in students:
        return{"Id":"Not Exist"}
    del students[student_id]
    return{"Message":"Student deleted"}

