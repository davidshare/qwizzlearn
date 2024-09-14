from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TagBase(BaseModel):
    name: str
    description: Optional[str]


class TagCreate(TagBase):
    pass


class TagRead(TagBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: datetime
    is_active: bool


class TagUpdate(TagBase):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
