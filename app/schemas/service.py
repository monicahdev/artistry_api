from datetime import datetime

from pydantic import BaseModel


class ServiceBase(BaseModel):
    service_name: str
    description: str | None = None
    photo: str | None = None
    price_from: float
    duration: int


class ServiceCreate(ServiceBase):
    pass

class ServiceRead(ServiceBase):
    id: int
    created_at: datetime | None = None

    class Config:
        from_attributes = True