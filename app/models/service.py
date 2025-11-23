from datetime import datetime

from app.db.base_class import Base
from sqlalchemy import Column, DateTime, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    photo = Column(String, nullable=True)
    price_from = Column(Numeric(10, 2), nullable=True)
    duration = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    bookings = relationship(
        "Booking",
        back_populates="service",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return f"<Service id={self.id} name={self.service_name!r}>"