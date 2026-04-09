from pydantic import BaseModel


class MembershipResponse(BaseModel):
    id: int
    user_id: int
    workspace_id: int
    role: str

    class Config:
        from_attributes = True