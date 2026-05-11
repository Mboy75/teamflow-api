from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Membership(Base):
    __tablename__ = "memberships"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    workspace_id = Column(
        Integer,
        ForeignKey("workspaces.id", ondelete="CASCADE"),
        nullable=False
    )

    # owner | admin | member | viewer
    role = Column(
        String,
        nullable=False,
        default="member"
    )

    # relationships
    user = relationship("User", back_populates="memberships")
    workspace = relationship("Workspace", back_populates="memberships")