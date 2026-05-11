from pydantic import BaseModel, ConfigDict


class MembershipResponse(BaseModel):
    id: int
    user_id: int
    workspace_id: int
    role: str

    model_config = ConfigDict(from_attributes=True)

class WorkspaceInvite(BaseModel):
    email: str
    role: str = "member"        