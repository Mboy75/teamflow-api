from sqlalchemy.orm import Session
from app.models.skill import Skill
from app.schemas.skill_schema import SkillCreate, SkillUpdate
from app.models.project import Project


def get_all_skills(db: Session):
    return db.query(Skill).all()


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
    if skill not in project.skills:
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