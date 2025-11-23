from app.db.base_class import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class UserClassAccess(Base):
    __tablename__ = "user_class_access"
    __table_args__ = (
        UniqueConstraint("user_id", "class_id", name="uq_user_class_access_user_class"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    class_id = Column(
        Integer,
        ForeignKey("online_classes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    granted_at = Column(DateTime(timezone=True), server_default=func.now())

    
    user = relationship("User", back_populates="class_access")
    online_class = relationship("OnlineClass", back_populates="user_access")

    def __repr__(self) -> str:
        return f"<UserClassAccess id={self.id} user_id={self.user_id} class_id={self.class_id}>"