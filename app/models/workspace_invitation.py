from datetime import datetime, timedelta
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.db.base import Base


class WorkspaceInvitation(Base):
    __tablename__ = "workspace_invitations"

    id = Column(Integer, primary_key=True, index=True)

    workspace_id = Column(Integer, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    invited_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    email = Column(String, index=True, nullable=False)
    role = Column(String, nullable=False, default="member")

    token = Column(String, unique=True, index=True, nullable=False)

    is_accepted = Column(Boolean, default=False)
    expires_at = Column(DateTime, nullable=False, default=lambda: datetime.utcnow() + timedelta(days=7))

    workspace = relationship("Workspace")
    invited_by = relationship("User")