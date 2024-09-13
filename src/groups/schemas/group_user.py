from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class GroupUserBase(BaseModel):
    group_id: int
    user_id: int
    role: str


class GroupUserCreate(GroupUserBase):
    pass


class GroupUserRead(GroupUserBase):
    id: Optional[int]  # Marking id as optional for read
    joined_at: datetime


class GroupUserUpdate(GroupUserBase):
    pass
