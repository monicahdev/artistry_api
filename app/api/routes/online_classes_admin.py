from app.dependencies import get_current_admin, get_db
from app.models.online_class import OnlineClass
from app.models.user import User
from app.schemas.online_class import OnlineClassCreate, OnlineClassRead
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

router = APIRouter()

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