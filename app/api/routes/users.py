from typing import List

from app.dependencies import get_current_admin, get_current_user
from app.dependencies_auth import authenticate_user, create_user_token, get_db
from app.models.user import User
from app.schemas.user import UserRead, UserUpdate
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/me")
def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "message": "Authenticated",
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "role": current_user.role,
        },
    }
    
@router.get("/all-users", response_model=list[UserRead])
def get_all_users(
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin),
):
    return db.query(User).all()

@router.patch("/me", response_model=UserRead)
def update_me(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if user_update.email is not None:
        user.email = user_update.email

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

