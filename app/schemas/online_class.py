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