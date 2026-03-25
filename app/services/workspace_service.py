from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.workspace import Workspace


def create_workspace(db: Session, name: str, slug: str, owner_id: int):
    existing_workspace = db.query(Workspace).filter(Workspace.slug == slug).first()
    if existing_workspace:
        raise HTTPException(status_code=400, detail="Workspace slug already exists")

    workspace = Workspace(
        name=name,
        slug=slug,
        owner_id=owner_id,
    )
    db.add(workspace)
    db.commit()
    db.refresh(workspace)
    return workspace


def get_user_workspaces(db: Session, user_id: int):
    return db.query(Workspace).filter(Workspace.owner_id == user_id).all()