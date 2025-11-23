from app.api.router import router as api_router
from app.db import base
from fastapi import FastAPI

app = FastAPI(
    title="Artistry by Sara MUA",
)

app.include_router(api_router)