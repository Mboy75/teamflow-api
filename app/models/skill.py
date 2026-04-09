from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.project_skill import project_skills


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True, index=True)
    level = Column(String(20), nullable=False)
    category = Column(String(30), nullable=False)
    years_of_experience = Column(Integer, nullable=False)

    projects = relationship(
        "Project",
        secondary=project_skills,
        back_populates="skills"
    )