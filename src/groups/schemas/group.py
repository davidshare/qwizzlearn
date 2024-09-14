from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from .group_user import GroupUserRead


class GroupBase(BaseModel):
    name: str
    description: Optional[str]


class GroupCreate(GroupBase):
    pass


class GroupRead(GroupBase):
    id: Optional[int]  # Marking id as optional for read
    created_by: int
    created_at: datetime
    updated_at: datetime
    users: Optional[List["GroupUserRead"]] = []  # Added list of related users


class GroupUpdate(GroupBase):
    pass
