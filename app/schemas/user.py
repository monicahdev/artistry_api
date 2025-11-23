from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    role: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserRead(UserBase):
    id: int
    created_at: datetime | None = None
    
    class Config:
        from_attributes = True

class Config:
    from_attributes = True  