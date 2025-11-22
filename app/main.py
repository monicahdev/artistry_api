from app.api.routes import router as api_router
from fastapi import FastAPI

app = FastAPI(
    title="Artistry by Sara MUA",
)

app.include_router(api_router)