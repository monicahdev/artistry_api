from datetime import datetime

from app.db.base_class import Base
from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class OnlineClass(Base):
    __tablename__ = "online_classes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    
    user_access = relationship(
        "UserClassAccess",
        back_populates="online_class",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return f"<OnlineClass id={self.id} name={self.name!r}>"