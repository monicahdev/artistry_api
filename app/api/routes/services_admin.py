from app.dependencies import get_current_admin
from app.dependencies_auth import get_current_admin, get_db
from app.models.service import Service
from app.models.user import User
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()

router = APIRouter(prefix="/admin/services", tags=["Admin - Services"])


@router.get("/")
def list_services_admin(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    services = db.query(Service).all()
    return services