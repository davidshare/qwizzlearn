from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from .user import User


class Token(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    refresh_token: str = Field(unique=True, index=True)
    issued_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime
    revoked: bool = Field(default=False)

    user: Optional["User"] = Relationship(back_populates="tokens")
