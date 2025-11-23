from datetime import datetime

from app.db.base_class import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    service_id = Column(
        Integer,
        ForeignKey("services.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    date_hour = Column(DateTime(timezone=True), nullable=False)
    comments = Column(Text, nullable=True)
    status = Column(String, nullable=False, default="PENDING")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    
    user = relationship("User", back_populates="bookings")
    service = relationship("Service", back_populates="bookings")

    def __repr__(self) -> str:
        return f"<Booking id={self.id} user_id={self.user_id} service_id={self.service_id} status={self.status!r}>"