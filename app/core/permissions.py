from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.deps import get_db, get_current_user
from app.models.membership import Membership
from app.models.user import User



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

# Predefined dependencies for common role checks

WorkspaceOwner = Depends(require_workspace_role(["owner"]))

WorkspaceAdmin = Depends(require_workspace_role(["owner", "admin"]))

WorkspaceMember = Depends(
    require_workspace_role(["owner", "admin", "member", "viewer"])
)