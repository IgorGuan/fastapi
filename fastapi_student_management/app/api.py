from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/students/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, group_id: int, db: Session = Depends(get_db)):
    return crud.create_student(db=db, student=student, group_id=group_id)

@app.post("/groups/", response_model=schemas.Group)
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    return crud.create_group(db=db, group=group)

@app.get("/students/{student_id}", response_model=schemas.Student)
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.get_student(db=db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@app.get("/groups/{group_id}", response_model=schemas.Group)
def read_group(group_id: int, db: Session = Depends(get_db)):
    db_group = crud.get_group(db=db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return db_group

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    crud.delete_student(db=db, student_id=student_id)
    return {"message": "Student deleted"}

@app.delete("/groups/{group_id}")
def delete_group(group_id: int, db: Session = Depends(get_db)):
    crud.delete_group(db=db, group_id=group_id)
    return {"message": "Group deleted"}

@app.get("/students/", response_model=list[schemas.Student])
def read_students(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    students = crud.get_students(db=db, skip=skip, limit=limit)
    return students

@app.get("/groups/", response_model=list[schemas.Group])
def read_groups(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    groups = crud.get_groups(db=db, skip=skip, limit=limit)
    return groups

@app.post("/groups/{group_id}/students/{student_id}")
def add_student_to_group(group_id: int, student_id: int, db: Session = Depends(get_db)):
    crud.add_student_to_group(db=db, student_id=student_id, group_id=group_id)
    return {"message": "Student added to group"}

@app.delete("/groups/{group_id}/students/{student_id}")
def remove_student_from_group(group_id: int, student_id: int, db: Session = Depends(get_db)):
    crud.remove_student_from_group(db=db, student_id=student_id)
    return {"message": "Student removed from group"}

@app.get("/groups/{group_id}/students/", response_model=list[schemas.Student])
def get_students_in_group(group_id: int, db: Session = Depends(get_db)):
    students = crud.get_students_in_group(db=db, group_id=group_id)
    return students

@app.post("/students/{student_id}/transfer/")
def transfer_student(student_id: int, new_group_id: int, db: Session = Depends(get_db)):
    crud.transfer_student(db=db, student_id=student_id, new_group_id=new_group_id)
    return {"message": "Student transferred"}
