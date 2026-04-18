from pydantic import BaseModel
#from app.schemas.skill_schema import SkillSimple
from app.schemas.skill_schema import SkillResponse


class ProjectCreate(BaseModel):
    name: str
    workspace_id: int


class ProjectResponse(BaseModel):
    id: int
    name: str
    workspace_id: int

    class Config:
        from_attributes = True

class ProjectWithSkills(ProjectResponse):
    skills: list[SkillResponse] = []

    class Config:
        from_attributes = True

    