from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_current_user, get_db
from app.schemas.membership import MembershipResponse
from app.services.membership_service import add_member_to_workspace, get_workspace_members

router = APIRouter(prefix="/memberships", tags=["Memberships"])


@router.post("/{workspace_id}", response_model=MembershipResponse)
def add_member(
    workspace_id: int,
    email: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return add_member_to_workspace(
        db=db,
        workspace_id=workspace_id,
        email=email,
        current_user_id=current_user.id,
    )


@router.get("/{workspace_id}", response_model=list[MembershipResponse])
def list_members(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_workspace_members(db, workspace_id)