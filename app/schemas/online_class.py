from datetime import datetime

from pydantic import BaseModel


class OnlineClassBase(BaseModel):
    name: str
    description: str
    url: str


class OnlineClassCreate(OnlineClassBase):
    pass


class OnlineClassRead(OnlineClassBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class OnlineClassUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    url: str | None = None
    
class UserClassAccessRead(BaseModel):
    id: int
    user_id: int
    class_id: int
    granted_at: datetime

    class Config:
        from_attributes = True