from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_current_user, get_db
from app.schemas.project import ProjectCreate, ProjectResponse
from app.services.project_service import create_project, get_workspace_projects
from app.models.project import Project

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectResponse)
def create_project_endpoint(
    data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return create_project(
        db=db,
        name=data.name,
        workspace_id=data.workspace_id,
        current_user_id=current_user.id,
    )


@router.get("/workspace/{workspace_id}", response_model=list[ProjectResponse])
def list_projects(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_workspace_projects(
        db=db,
        workspace_id=workspace_id,
        current_user_id=current_user.id,
    )


# temporary ro get project list without authentication and workspace filtering, to be used in the frontend until we implement the full project management features

@router.get("/")
def get_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()