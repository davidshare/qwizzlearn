from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class GroupBase(BaseModel):
    name: str
    description: Optional[str]


class GroupCreate(GroupBase):
    created_by: int


class GroupRead(GroupBase):
    id: Optional[int]  # Marking id as optional for read
    created_by: int
    created_at: datetime
    updated_at: datetime
    users: Optional[List["GroupUserRead"]] = []  # Added list of related users


class GroupUpdate(GroupBase):
    pass


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
