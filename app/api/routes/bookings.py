from fastapi import APIRouter

router = APIRouter()

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
        status="PENDING",
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return booking