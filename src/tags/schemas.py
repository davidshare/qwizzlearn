from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TagBase(BaseModel):
    name: str
    description: Optional[str]


class TagCreate(TagBase):
    created_by: int


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
