from pydantic import BaseModel, ConfigDict


class WorkspaceCreate(BaseModel):
    name: str
    slug: str


class WorkspaceResponse(BaseModel):
    id: int
    name: str
    slug: str
    owner_id: int

    model_config = ConfigDict(from_attributes=True)