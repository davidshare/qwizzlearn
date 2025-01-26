from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from .user import User


class Session(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    session_token: str = Field(unique=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime
    device_info: str

    user: Optional["User"] = Relationship(back_populates="sessions")
