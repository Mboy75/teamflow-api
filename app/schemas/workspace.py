from pydantic import BaseModel


class WorkspaceCreate(BaseModel):
    name: str
    slug: str


class WorkspaceResponse(BaseModel):
    id: int
    name: str
    slug: str
    owner_id: int

    class Config:
        from_attributes = True