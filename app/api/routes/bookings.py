from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.models.booking import Booking
from app.models.service import Service
from app.models.user import User
from app.schemas.booking import BookingCreate, BookingRead, BookingUpdate

router = APIRouter()

@router.get("/me", response_model=List[BookingRead])
def list_my_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    bookings = (
        db.query(Booking)
        .filter(Booking.user_id == current_user.id)
        .order_by(Booking.date_hour.desc())
        .all()
    )
    return bookings

@router.post("/", response_model=BookingRead, status_code=status.HTTP_201_CREATED)
def create_booking(
    booking_in: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    
    if current_user.role != "USER":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only role USER can create bookings",
        )

    
    service = db.query(Service).filter(Service.id == booking_in.service_id).first()
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found",
        )

    booking = Booking(
        user_id=current_user.id,
        service_id=booking_in.service_id,
        date_hour=booking_in.date_hour,
        comments=booking_in.comments,
        status="CREATED",
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return booking


@router.patch("/{booking_id}", response_model=BookingRead)
def update_booking(
    booking_id: int,
    booking_in: BookingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    
    #is_admin = current_user.role == "ADMIN"
    is_owner = booking.user_id == current_user.id

    #if not (is_admin or is_owner):
    if not (is_owner):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this booking",
        )

    
    #if booking_in.status is not None and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can change booking status",
        )

    
    if booking_in.date_hour is not None:
        booking.date_hour = booking_in.date_hour

    if booking_in.comments is not None:
        booking.comments = booking_in.comments

    #if is_admin and booking_in.status is not None:
    if booking_in.status is not None:
        booking.status = booking_in.status

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return booking


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if current_user.role != "ADMIN" and booking.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized to delete this booking",
        )

    db.delete(booking)
    db.commit()
    
    return