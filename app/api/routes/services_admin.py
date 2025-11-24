from app.dependencies import get_current_admin, get_db
from app.models.service import Service
from app.models.user import User
from app.schemas.service import ServiceCreate, ServiceRead
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/")
def list_services_admin(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    services = db.query(Service).all()
    return services

@router.post("/", response_model=ServiceRead, status_code=status.HTTP_201_CREATED)
def create_service(
    service_in: ServiceCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    service = Service(**service_in.model_dump())
    db.add(service)
    db.commit()
    db.refresh(service)
    return service