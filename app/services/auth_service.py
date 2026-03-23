from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.services.user_service import get_user_by_email


def login_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "message": "Login successful",
        "user_id": user.id,
        "email": user.email,
    }