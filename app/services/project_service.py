from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.project import Project
from app.services.permission_service import (
    require_workspace_member,
    require_workspace_owner,
)


def create_project(db: Session, name: str, workspace_id: int, current_user_id: int):
    require_workspace_owner(db, workspace_id, current_user_id)

    project = Project(
        name=name,
        workspace_id=workspace_id
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


def get_workspace_projects(db: Session, workspace_id: int, current_user_id: int):
    require_workspace_member(db, workspace_id, current_user_id)

    return db.query(Project).filter(
        Project.workspace_id == workspace_id
    ).all()