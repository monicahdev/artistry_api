from app.dependencies import get_db
from app.models.service import Service
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/services", tags=["Services"])

@router.get("/")
def list_services(db: Session = Depends(get_db)):
    services = db.query(Service).all()
    return services