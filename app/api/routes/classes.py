from typing import List

from app.dependencies import (get_current_user, get_current_user_optional,
                              get_db)
from app.models.online_class import OnlineClass
from app.models.user import User
from app.models.user_class_access import UserClassAccess
from app.schemas.online_class import OnlineClassRead
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/", response_model=List[OnlineClassRead])
def list_online_classes(
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    if current_user and current_user.role == "ADMIN":
        return db.query(OnlineClass).all()

    if current_user:
        return (
            db.query(OnlineClass)
            .join(UserClassAccess, OnlineClass.id == UserClassAccess.class_id)
            .filter(UserClassAccess.user_id == current_user.id)
            .all()
        )

    return []