from app.dependencies import get_current_user
from app.models.user import User
from fastapi import APIRouter, Depends

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