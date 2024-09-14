from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CategoryBase(BaseModel):
    name: str
    description: Optional[str]


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: datetime
    is_active: bool


class CategoryUpdate(CategoryBase):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
