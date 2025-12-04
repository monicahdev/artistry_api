from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import router as api_router
from app.db import base

app = FastAPI(
    title="Artistry by Sara MUA",
)

origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "https://artistrybysaramua.netlify.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)