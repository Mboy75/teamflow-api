from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.membership import Membership
from app.models.workspace import Workspace


def require_workspace_owner(db: Session, workspace_id: int, user_id: int):
    workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()

    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")

    if workspace.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return workspace


def require_workspace_member(db: Session, workspace_id: int, user_id: int):
    workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()

    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")

    if workspace.owner_id == user_id:
        return True

    membership = db.query(Membership).filter(
        Membership.workspace_id == workspace_id,
        Membership.user_id == user_id
    ).first()

    if not membership:
        raise HTTPException(status_code=403, detail="Not a workspace member")

    return True