from pydantic import BaseModel, Field
from typing import Optional


class SkillBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    level: str = Field(..., min_length=2, max_length=20)
    category: str = Field(..., min_length=2, max_length=30)
    years_of_experience: int = Field(..., ge=0, le=50)


class SkillCreate(SkillBase):
    pass


class SkillUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    level: Optional[str] = Field(None, min_length=2, max_length=20)
    category: Optional[str] = Field(None, min_length=2, max_length=30)
    years_of_experience: Optional[int] = Field(None, ge=0, le=50)


class SkillResponse(SkillBase):
    id: int

    class Config:
        from_attributes = True