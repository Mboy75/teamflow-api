from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.deps import get_current_user, get_db
from app.schemas.workspace import WorkspaceCreate, WorkspaceResponse
from app.services.workspace_service import create_workspace, get_user_workspaces
from app.models.user import User
from app.models.workspace import Workspace
from app.models.membership import Membership
from app.utils.permissions import get_workspace_membership, require_workspace_member, require_workspace_owner_or_admin


router = APIRouter(prefix="/workspaces", tags=["Workspaces"])


@router.post("/", response_model=WorkspaceResponse)
def create_workspace_endpoint(
    data: WorkspaceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return create_workspace(
        db=db,
        name=data.name,
        slug=data.slug,
        owner_id=current_user.id,
    )


@router.get("/", response_model=list[WorkspaceResponse])
def list_workspaces_endpoint(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_user_workspaces(db, current_user.id)


@router.get("/{workspace_id}", response_model=WorkspaceResponse)
def get_workspace(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    membership = Depends(require_workspace_member)
):
    workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()

    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found"
        )

    get_workspace_membership(
        db=db,
        user_id=current_user.id,
        workspace_id=workspace_id
    )

    return workspace




@router.delete("/{workspace_id}")
def delete_workspace(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    membership = Depends(require_workspace_owner_or_admin)
):
    workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()

    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found"
        )

    get_workspace_membership(
        db=db,
        user_id=current_user.id,
        workspace_id=workspace_id,
        allowed_roles=["owner", "admin"]
    )

    db.delete(workspace)
    db.commit()

    return {"message": "Workspace deleted successfully"}