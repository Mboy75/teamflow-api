from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.models.membership import Membership
from app.models.user import User
from app.db.deps import get_current_user


def require_workspace_role(allowed_roles: list[str]):
    def role_checker(
        workspace_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        membership = (
            db.query(Membership)
            .filter(
                Membership.workspace_id == workspace_id,
                Membership.user_id == current_user.id,
            )
            .first()
        )

        if not membership:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not a workspace member",
            )

        if membership.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return membership

    return role_checker