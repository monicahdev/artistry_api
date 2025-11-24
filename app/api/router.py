from app.api.routes import (auth, bookings, classes, services, services_admin,
                            users)
from fastapi import APIRouter

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(services.router, prefix="/services", tags=["Services"])
router.include_router(classes.router, prefix="/classes", tags=["Classes"])
router.include_router(bookings.router, prefix="/bookings", tags=["Bookings"])
router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(services_admin.router, prefix="/admin/services", tags=["Admin - services"]) 