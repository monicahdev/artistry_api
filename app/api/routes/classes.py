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

@router.get("/{class_id}", response_model=OnlineClassRead)
def get_class_detail(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    online_class = db.query(OnlineClass).filter(OnlineClass.id == class_id).first()
    if not online_class:
        raise HTTPException(status_code=404, detail="Class not found")

    if current_user.role == "ADMIN":
        return online_class

    access = (
        db.query(UserClassAccess)
        .filter_by(user_id=current_user.id, class_id=class_id)
        .first()
    )
    if not access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this class",
        )

    return online_class