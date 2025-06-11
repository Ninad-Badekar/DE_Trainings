from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Employee(BaseModel):
    id:int
    name:str
    role:str

emps : List[Employee]=[] 

@app.get('/')
def greet():
    return {'Welcome': 'Employee Data'}

@app.get('/allEmp')
def get_emp():
    return emps

@app.post('/addEmp')
def add_emp(emp:Employee):
    emps.append(emp)
    return emp + "was added"

@app.put('/allEmp/{emp_id}')
def update_emp(emp_id:int,updated_emp:Employee):
    for index,item in enumerate(emps):
        if item.id == emp_id:
            emps[index] = updated_emp
            return updated_emp
    return {'error':'employee not found'}

@app.delete('/allEmp/{emp_id}')
def delete_emp(emp_id:int):
    for index,item in enumerate(emps):
        if item.id == emp_id:
            deleted = emps.pop(index)
            return deleted
    return {'error':'emp not found'}