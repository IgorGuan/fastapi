from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None

class LoginHistoryResponse(BaseModel):
    user_agent: str
    datetime: datetime

class UserResponse(BaseModel):
    id: int
    email: str
    login_history: List[LoginHistoryResponse] = []

    class Config:
        orm_mode = True
