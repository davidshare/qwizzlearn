from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship


class Device(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    device_id: str = Field(unique=True, index=True)
    device_type: str
    last_used_at: datetime = Field(default_factory=datetime.utcnow)
    is_trusted: bool = Field(default=False)

    user: Optional["User"] = Relationship(back_populates="devices")
