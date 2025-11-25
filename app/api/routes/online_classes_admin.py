from typing import List

from app.dependencies import get_current_admin, get_db
from app.models.online_class import OnlineClass
from app.models.user import User
from app.schemas.online_class import (OnlineClassCreate, OnlineClassRead,
                                      OnlineClassUpdate)
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/", response_model=List[OnlineClassRead])
def list_online_classes(db: Session = Depends(get_db)):
    
    classes = db.query(OnlineClass).all()
    return classes

@router.post("/", response_model=OnlineClassRead, status_code=status.HTTP_201_CREATED)
def create_online_class(
    class_in: OnlineClassCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    online_class = OnlineClass(**class_in.model_dump())

    db.add(online_class)
    db.commit()
    db.refresh(online_class)

    return online_class


@router.patch("/{class_id}", response_model=OnlineClassRead)
def update_online_class(
    class_id: int,
    class_in: OnlineClassUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    online_class = db.query(OnlineClass).filter(OnlineClass.id == class_id).first()
    if not online_class:
        raise HTTPException(status_code=404, detail="Class not found")

    update_data = class_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(online_class, field, value)

    db.commit()
    db.refresh(online_class)
    return online_class

@router.delete("/{class_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_online_class(
    class_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    online_class = db.query(OnlineClass).filter(OnlineClass.id == class_id).first()
    if not online_class:
        raise HTTPException(status_code=404, detail="Class not found")

    db.delete(online_class)
    db.commit()