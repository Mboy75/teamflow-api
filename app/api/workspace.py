from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_current_user, get_db
from app.schemas.workspace import WorkspaceCreate, WorkspaceResponse
from app.services.workspace_service import create_workspace, get_user_workspaces

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