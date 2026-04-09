from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.deps import get_current_user
from app.schemas.task import TaskCreate, TaskOut
from app.services.task_service import (
    create_task,
    get_tasks_by_project,
    update_task_status,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskOut)
def create(
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return create_task(db, data, current_user.id)


@router.get("/project/{project_id}")
def get_tasks(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_tasks_by_project(db, project_id, current_user.id)


@router.put("/{task_id}/status")
def update_status(
    task_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return update_task_status(
        db=db,
        task_id=task_id,
        status=status,
        current_user_id=current_user.id,
    )