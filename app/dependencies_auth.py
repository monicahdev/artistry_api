from datetime import timedelta

from app.config import settings
from app.db.session import SessionLocal
from app.models.user import User
from app.security import create_access_token, verify_password
from fastapi import Depends
from sqlalchemy.orm import Session


def get_db():
    # get db session
    
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    # check mail & pwd. returned if correct
    
    user: User | None = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def create_user_token(user: User) -> str:
    # create token for user according to role
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"sub": str(user.id), "role": user.role},
        expires_delta=access_token_expires,
    )
    return token