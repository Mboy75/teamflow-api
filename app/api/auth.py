from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.schemas.auth import LoginRequest
from app.schemas.token import TokenResponse
from app.services.auth_service import login_user

from app.db.deps import get_current_user
from app.schemas.user import UserResponse

router = APIRouter(prefix="/auth", tags=["Auth"])




@router.post("/login", response_model=TokenResponse)
def login_endpoint(data: LoginRequest, db: Session = Depends(get_db)):
    return login_user(db, data.email, data.password)


@router.get("/me", response_model=UserResponse)
def get_me(current_user = Depends(get_current_user)):
    return current_user