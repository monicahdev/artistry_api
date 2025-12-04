import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL") or settings.DATABASE_URL

if not SQLALCHEMY_DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set.")


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 