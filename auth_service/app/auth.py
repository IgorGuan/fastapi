from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="邮箱已被注册")
    hashed_password = utils.get_password_hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="邮箱或密码错误")

    access_token = utils.create_access_token(data={"sub": user.email})
    refresh_token = utils.create_refresh_token(data={"sub": user.email})

    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/refresh")
def refresh_token(refresh_token: str):

    pass


@router.put("/user/update")
def update_user(user: schemas.UserUpdate, db: Session = Depends(get_db)):

    pass


@router.get("/user/history")
def get_login_history(db: Session = Depends(get_db)):

    pass


@router.post("/logout")
def logout():

    pass
