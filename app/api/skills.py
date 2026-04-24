from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.models.project import Project
from app.db.session import get_db
from app.schemas.skill_schema import SkillCreate, SkillUpdate, SkillResponse, SkillListResponse
from app.services.skill_service import (
    get_all_skills,
    get_skill_by_id,
    get_skill_by_name,
    create_skill,
    update_skill,
    delete_skill,
    add_skill_to_project,
    remove_skill_from_project,
)

from app.db.deps import get_current_user, get_db
from app.models.user import User
from app.db.deps import require_admin_or_owner


router = APIRouter(prefix="/skills", tags=["Skills"])


@router.get("/", response_model=SkillListResponse)
def read_skills(
    category: str | None = None,
    level: str | None = None,
    search: str | None = None,
    skip: int = 0,
    limit: int = Query(default=10, le=100),
    sort_by: str | None = None,
    order: str = "asc",
    db: Session = Depends(get_db)
):
    return get_all_skills(
        db,
        category=category,
        level=level,
        search=search,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        order=order
    )


@router.get("/{skill_id}", response_model=SkillResponse)
def read_skill(skill_id: int, db: Session = Depends(get_db)):
    skill = get_skill_by_id(db, skill_id)

    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )

    return skill


@router.post("/", response_model=SkillResponse, status_code=status.HTTP_201_CREATED)
def create_new_skill(
    skill: SkillCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_skill = get_skill_by_name(db, skill.name)

    if existing_skill:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Skill already exists"
        )

    return create_skill(db, skill)


@router.put("/{skill_id}", response_model=SkillResponse)
def update_existing_skill(
    skill_id: int,
    skill_data: SkillUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    skill = get_skill_by_id(db, skill_id)

    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )

    if skill_data.name is not None:
        existing_skill = get_skill_by_name(db, skill_data.name)

        if existing_skill and existing_skill.id != skill_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Another skill with this name already exists"
            )

    return update_skill(db, skill, skill_data)


@router.delete("/{skill_id}")
def delete_existing_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    skill = get_skill_by_id(db, skill_id)

    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    delete_skill(db, skill)

    return {"message": "Skill deleted successfully"}

@router.post("/projects/{project_id}/skills/{skill_id}")
def assign_skill_to_project(
    project_id: int,
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    require_admin_or_owner(current_user, project.workspace_id, db)

    skill = get_skill_by_id(db, skill_id)

    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    add_skill_to_project(db, project, skill)

    return {
        "message": f"Skill {skill.name} assigned to project {project.name}"
    }

@router.get("/projects/{project_id}/skills", response_model=list[SkillResponse])
def get_project_skills(
    project_id: int,
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project.skills

@router.delete("/projects/{project_id}/skills/{skill_id}")
def unassign_skill_from_project(
    project_id: int,
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    require_admin_or_owner(current_user, project.workspace_id, db)

    skill = get_skill_by_id(db, skill_id)

    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    remove_skill_from_project(db, project, skill)

    return {
        "message": f"Skill {skill.name} removed from project {project.name}"
    }
