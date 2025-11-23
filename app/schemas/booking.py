from app.dependencies_auth import get_current_user, get_db
from app.models.booking import Booking
from app.models.user import User
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("/")
def list_my_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    bookings = (
        db.query(Booking)
        .filter(Booking.user_id == current_user.id)
        .all()
    )
    return bookings