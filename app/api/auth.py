from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.schemas.auth import LoginRequest
from app.services.auth_service import login_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login_endpoint(data: LoginRequest, db: Session = Depends(get_db)):
    return login_user(db, data.email, data.password)