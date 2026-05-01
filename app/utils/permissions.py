from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.models.membership import Membership

from app.db.deps import get_db, get_current_user
from app.models.user import User


def get_workspace_membership(
    db: Session,
    user_id: int,
    workspace_id: int,
    allowed_roles: list[str] | None = None,
):
    membership = db.query(Membership).filter(
        Membership.user_id == user_id,
        Membership.workspace_id == workspace_id
    ).first()

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this workspace"
        )

    if allowed_roles and membership.role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )

    return membership


def require_workspace_member(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_workspace_membership(
        db=db,
        user_id=current_user.id,
        workspace_id=workspace_id
    )


def require_workspace_owner_or_admin(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_workspace_membership(
        db=db,
        user_id=current_user.id,
        workspace_id=workspace_id,
        allowed_roles=["owner", "admin"]
    )