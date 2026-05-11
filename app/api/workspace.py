from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.deps import get_db, get_current_user
from app.models.user import User
from app.models.workspace import Workspace
from app.models.membership import Membership
from app.schemas.workspace import WorkspaceCreate, WorkspaceResponse
from app.core.permissions import require_workspace_role

router = APIRouter(
    prefix="/workspaces",
    tags=["Workspaces"]
)


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

    workspace_ids = [membership.workspace_id for membership in memberships]

    return (
        db.query(Workspace)
        .filter(Workspace.id.in_(workspace_ids))
        .all()
    )


@router.post("/", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
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

    membership = Membership(
        user_id=current_user.id,
        workspace_id=workspace.id,
        role="owner"
    )

    db.add(membership)
    db.commit()

    return workspace


@router.get("/{workspace_id}", response_model=WorkspaceResponse)
def get_workspace(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    membership: Membership = Depends(require_workspace_role(["owner", "admin", "member", "viewer"]))
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


@router.delete("/{workspace_id}")
def delete_workspace(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    membership: Membership = Depends(require_workspace_role(["owner"]))
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

    return {"message": "Workspace deleted successfully"}