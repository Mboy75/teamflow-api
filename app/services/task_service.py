from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.task import Task
from app.services.permission_service import require_workspace_member


def create_task(db: Session, data, current_user_id: int):
    project = db.query(Project).filter(Project.id == data.project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    require_workspace_member(
        db=db,
        workspace_id=project.workspace_id,
        user_id=current_user_id,
    )

    task = Task(**data.dict())

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_tasks_by_project(db: Session, project_id: int, current_user_id: int):
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    require_workspace_member(
        db=db,
        workspace_id=project.workspace_id,
        user_id=current_user_id,
    )

    return db.query(Task).filter(Task.project_id == project_id).all()


def update_task_status(
    db: Session,
    task_id: int,
    status: str,
    current_user_id: int,
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    project = db.query(Project).filter(Project.id == task.project_id).first()

    require_workspace_member(
        db=db,
        workspace_id=project.workspace_id,
        user_id=current_user_id,
    )

    task.status = status

    db.commit()
    db.refresh(task)

    return task