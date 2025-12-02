from app.dependencies_auth import authenticate_user, create_user_token, get_db
from app.models.user import User
from app.schemas.auth import Token, UserLogin, UserRegister
from app.security import get_password_hash
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()
from fastapi import APIRouter

router = APIRouter()


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register_user(
    user_in: UserRegister,
    db: Session = Depends(get_db),
):
    # Check if email exists
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with that email already exists",
        )

    user = User(
        email=user_in.email,
        password_hash=get_password_hash(user_in.password),
        role="USER",
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Create token for user auth
    access_token = create_user_token(user)
    return Token(access_token=access_token)


@router.post("/login", response_model=Token)
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong email or password.",
            headers={"Auth": "Bearer"},
        )

    access_token = create_user_token(user)
    return Token(access_token=access_token)