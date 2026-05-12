from pydantic import BaseModel, ConfigDict, EmailStr


class MembershipResponse(BaseModel):
    id: int
    user_id: int
    workspace_id: int
    role: str

    model_config = ConfigDict(from_attributes=True)


class WorkspaceInvite(BaseModel):
    email: EmailStr
    role: str = "member"


class WorkspaceInvitationCreate(BaseModel):
    email: EmailStr
    role: str = "member"


class WorkspaceInvitationResponse(BaseModel):
    id: int
    workspace_id: int
    email: EmailStr
    role: str
    token: str
    is_accepted: bool

    model_config = ConfigDict(from_attributes=True)     