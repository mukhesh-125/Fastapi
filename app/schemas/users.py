from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreateModel(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOutModel(BaseModel):
    id : int
    username : str
    email : EmailStr
    created_at: datetime
    class Config: from_attributes = True

