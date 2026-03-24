from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.schemas.token import TokenResponse
from app.services.user_service import get_user_by_email


def login_user(db: Session, email: str, password: str) -> TokenResponse:
    user = get_user_by_email(db, email)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )