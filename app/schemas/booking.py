from datetime import datetime

from pydantic import BaseModel


class BookingBase(BaseModel):
    service_id: int
    date_hour: datetime
    comments: str | None = None


class BookingCreate(BookingBase):
    pass

class BookingRead(BookingBase):
    id: int
    user_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True