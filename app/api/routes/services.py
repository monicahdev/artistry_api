from typing import List

from app.dependencies import get_db
from app.models.service import Service
from app.schemas.service import ServiceRead
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/", response_model=List[ServiceRead])
def list_services(db: Session = Depends(get_db)):
    services = db.query(Service).all()
    return services

@router.get("/{service_id}", response_model=ServiceRead)
def get_service_detail(
    service_id: int,
    db: Session = Depends(get_db),
):
    
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found",
        )
    return service