from app.api.routes import auth, bookings, classes, services, users
from fastapi import APIRouter

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(services.router, prefix="/services", tags=["services"])
router.include_router(classes.router, prefix="/classes", tags=["classes"])
router.include_router(bookings.router, prefix="/bookings", tags=["bookings"])
router.include_router(users.router, prefix="/users", tags=["users"])
