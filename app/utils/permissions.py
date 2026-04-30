from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.membership import Membership


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