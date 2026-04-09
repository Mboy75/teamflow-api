from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.membership import Membership
from app.services.permission_service import require_workspace_owner
from app.services.user_service import get_user_by_email


def add_member_to_workspace(db: Session, workspace_id: int, email: str, current_user_id: int):
    require_workspace_owner(db, workspace_id, current_user_id)

    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    existing = db.query(Membership).filter(
        Membership.user_id == user.id,
        Membership.workspace_id == workspace_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="User already in workspace")

    membership = Membership(
        user_id=user.id,
        workspace_id=workspace_id,
        role="member"
    )

    db.add(membership)
    db.commit()
    db.refresh(membership)
    return membership


def get_workspace_members(db: Session, workspace_id: int):
    return db.query(Membership).filter(
        Membership.workspace_id == workspace_id
    ).all()