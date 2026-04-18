from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.services.user_service import get_user_by_email
from app.models.membership import Membership

security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user

def require_admin_or_owner(current_user, workspace_id, db):
    membership = (
        db.query(Membership)
        .filter(
            Membership.user_id == current_user.id,
            Membership.workspace_id == workspace_id
        )
        .first()
    )
# only for debugging purposes, remove in production
    print("DEBUG current_user.id =", current_user.id)
    print("DEBUG workspace_id =", workspace_id)
    print("DEBUG membership =", membership)
#end of debugging
    if not membership:
        raise HTTPException(
            status_code=403,
            detail="You are not a member of this workspace"
        )

    if membership.role not in ["owner", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to perform this action"
        )

    return membership