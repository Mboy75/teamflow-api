from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.skill import Skill
from app.schemas.skill_schema import SkillCreate, SkillUpdate
from app.models.project import Project


def get_all_skills(
    db: Session,
    category: str | None = None,
    level: str | None = None,
    search: str | None = None,
    skip: int = 0,
    limit: int = 10,
    sort_by: str | None = None,
    order: str = "asc",
):
    query = db.query(Skill)

    if category:
        query = query.filter(Skill.category.ilike(category))

    if level:
        query = query.filter(Skill.level.ilike(level))

    if search:
        query = query.filter(Skill.name.ilike(f"%{search}%"))

    if sort_by:
        allowed_fields = ["name", "level", "category", "years_of_experience"]

        if sort_by in allowed_fields:
            column = getattr(Skill, sort_by)

        if order == "desc":
            query = query.order_by(column.desc())
        else:
            query = query.order_by(column.asc())

    return query.offset(skip).limit(limit).all()


def get_skill_by_id(db: Session, skill_id: int):
    return db.query(Skill).filter(Skill.id == skill_id).first()


def get_skill_by_name(db: Session, name: str):
    return db.query(Skill).filter(Skill.name.ilike(name)).first()


def create_skill(db: Session, skill_data: SkillCreate):
    skill = Skill(
        name=skill_data.name,
        level=skill_data.level,
        category=skill_data.category,
        years_of_experience=skill_data.years_of_experience,
    )
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill


def update_skill(db: Session, skill: Skill, skill_data: SkillUpdate):
    if skill_data.name is not None:
        skill.name = skill_data.name

    if skill_data.level is not None:
        skill.level = skill_data.level

    if skill_data.category is not None:
        skill.category = skill_data.category

    if skill_data.years_of_experience is not None:
        skill.years_of_experience = skill_data.years_of_experience

    db.commit()
    db.refresh(skill)
    return skill


def delete_skill(db: Session, skill: Skill):
    db.delete(skill)
    db.commit()




def add_skill_to_project(db, project: Project, skill: Skill):
    if skill in project.skills:
        raise HTTPException(
            status_code=400,
            detail="Skill already assigned to this project"
        )

    project.skills.append(skill)
    db.commit()
    db.refresh(project)

    return project


def remove_skill_from_project(db, project: Project, skill: Skill):
    if skill in project.skills:
        project.skills.remove(skill)
        db.commit()
        db.refresh(project)

    return project    