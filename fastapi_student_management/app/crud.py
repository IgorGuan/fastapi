from sqlalchemy.orm import Session
from . import models, schemas

def create_student(db: Session, student: schemas.StudentCreate, group_id: int):
    db_student = models.Student(name=student.name, group_id=group_id)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def create_group(db: Session, group: schemas.GroupCreate):
    db_group = models.Group(name=group.name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

def get_group(db: Session, group_id: int):
    return db.query(models.Group).filter(models.Group.id == group_id).first()

def delete_student(db: Session, student_id: int):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    db.delete(db_student)
    db.commit()

def delete_group(db: Session, group_id: int):
    db_group = db.query(models.Group).filter(models.Group.id == group_id).first()
    db.delete(db_group)
    db.commit()

def get_students(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Student).offset(skip).limit(limit).all()

def get_groups(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Group).offset(skip).limit(limit).all()

def add_student_to_group(db: Session, student_id: int, group_id: int):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    student.group_id = group_id
    db.commit()

def remove_student_from_group(db: Session, student_id: int):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    student.group_id = None
    db.commit()

def get_students_in_group(db: Session, group_id: int):
    return db.query(models.Student).filter(models.Student.group_id == group_id).all()

def transfer_student(db: Session, student_id: int, new_group_id: int):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    student.group_id = new_group_id
    db.commit()
