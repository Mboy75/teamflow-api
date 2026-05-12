from datetime import datetime
import secrets

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.deps import get_db, get_current_user

from app.models.user import User
from app.models.workspace import Workspace
from app.models.membership import Membership
from app.models.workspace_invitation import WorkspaceInvitation

from app.schemas.workspace import WorkspaceCreate, WorkspaceResponse
from app.schemas.membership import (
    WorkspaceInvite,
    WorkspaceInvitationCreate,
    WorkspaceInvitationResponse,
)

from app.core.permissions import (
    WorkspaceOwner,
    WorkspaceAdmin,
    WorkspaceMember,
)


router = APIRouter(
    prefix="/workspaces",
    tags=["Workspaces"]
)


# =========================
# LIST WORKSPACES
# =========================
@router.get("/", response_model=list[WorkspaceResponse])
def list_workspaces(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    memberships = (
        db.query(Membership)
        .filter(Membership.user_id == current_user.id)
        .all()
    )

    workspace_ids = [
        membership.workspace_id
        for membership in memberships
    ]

    workspaces = (
        db.query(Workspace)
        .filter(Workspace.id.in_(workspace_ids))
        .all()
    )

    return workspaces


# =========================
# CREATE WORKSPACE
# =========================
@router.post(
    "/",
    response_model=WorkspaceResponse,
    status_code=status.HTTP_201_CREATED
)
def create_workspace(
    workspace_data: WorkspaceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    workspace = Workspace(
        name=workspace_data.name,
        slug=workspace_data.slug,
        owner_id=current_user.id
    )

    db.add(workspace)
    db.commit()
    db.refresh(workspace)

    owner_membership = Membership(
        user_id=current_user.id,
        workspace_id=workspace.id,
        role="owner"
    )

    db.add(owner_membership)
    db.commit()

    return workspace


# =========================
# GET WORKSPACE
# =========================
@router.get(
    "/{workspace_id}",
    response_model=WorkspaceResponse
)
def get_workspace(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    membership: Membership = WorkspaceMember
):
    workspace = (
        db.query(Workspace)
        .filter(Workspace.id == workspace_id)
        .first()
    )

    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found"
        )

    return workspace


# =========================
# INVITE USER
# =========================
@router.post("/{workspace_id}/invite")
def invite_user_to_workspace(
    workspace_id: int,
    invite_data: WorkspaceInvite,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    membership: Membership = WorkspaceAdmin
):
    workspace = (
        db.query(Workspace)
        .filter(Workspace.id == workspace_id)
        .first()
    )

    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found"
        )

    user = (
        db.query(User)
        .filter(User.email == invite_data.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this email not found"
        )

    if invite_data.role not in [
        "admin",
        "member",
        "viewer"
    ]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role"
        )

    existing_membership = (
        db.query(Membership)
        .filter(
            Membership.user_id == user.id,
            Membership.workspace_id == workspace_id
        )
        .first()
    )

    if existing_membership:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a member of this workspace"
        )

    new_membership = Membership(
        user_id=user.id,
        workspace_id=workspace_id,
        role=invite_data.role
    )

    db.add(new_membership)
    db.commit()
    db.refresh(new_membership)

    return {
        "message": "User added to workspace successfully",
        "workspace_id": workspace_id,
        "user_id": user.id,
        "role": new_membership.role
    }


# =========================
# DELETE WORKSPACE
# =========================
@router.delete("/{workspace_id}")
def delete_workspace(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    membership: Membership = WorkspaceOwner
):
    workspace = (
        db.query(Workspace)
        .filter(Workspace.id == workspace_id)
        .first()
    )

    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found"
        )

    db.delete(workspace)
    db.commit()

    return {
        "message": "Workspace deleted successfully"
    }



@router.post(
    "/{workspace_id}/invitations",
    response_model=WorkspaceInvitationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_workspace_invitation(
    workspace_id: int,
    invite_data: WorkspaceInvitationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    membership: Membership = WorkspaceAdmin,
):
    if invite_data.role not in ["admin", "member", "viewer"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")

    existing_invitation = (
        db.query(WorkspaceInvitation)
        .filter(
            WorkspaceInvitation.workspace_id == workspace_id,
            WorkspaceInvitation.email == invite_data.email,
            WorkspaceInvitation.is_accepted == False,
        )
        .first()
    )

    if existing_invitation:
        raise HTTPException(status_code=400, detail="Pending invitation already exists")

    token = secrets.token_urlsafe(32)

    invitation = WorkspaceInvitation(
        workspace_id=workspace_id,
        invited_by_user_id=current_user.id,
        email=invite_data.email,
        role=invite_data.role,
        token=token,
    )

    db.add(invitation)
    db.commit()
    db.refresh(invitation)

    invite_link = f"http://localhost:8000/workspaces/invitations/accept/{token}"

    return invitation



@router.post("/invitations/accept/{token}")
def accept_workspace_invitation(
    token: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    invitation = (
        db.query(WorkspaceInvitation)
        .filter(WorkspaceInvitation.token == token)
        .first()
    )

    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")

    if invitation.is_accepted:
        raise HTTPException(status_code=400, detail="Invitation already accepted")

    if invitation.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invitation expired")

    if invitation.email != current_user.email:
        raise HTTPException(status_code=403, detail="This invitation is not for your account")

    existing_membership = (
        db.query(Membership)
        .filter(
            Membership.workspace_id == invitation.workspace_id,
            Membership.user_id == current_user.id,
        )
        .first()
    )

    if existing_membership:
        raise HTTPException(status_code=400, detail="User is already a member")

    membership = Membership(
        workspace_id=invitation.workspace_id,
        user_id=current_user.id,
        role=invitation.role,
    )

    invitation.is_accepted = True

    db.add(membership)
    db.commit()

    return {
        "message": "Invitation accepted successfully",
        "workspace_id": invitation.workspace_id,
        "role": invitation.role,
    }