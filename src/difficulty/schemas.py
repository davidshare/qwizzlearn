from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class DifficultyCreate(BaseModel):
    name: str = "easy"
    description: str = "Easy level of difficulty"


class DifficultyRead(DifficultyCreate):
    created_at: datetime
    updated_at: datetime


class DifficultyUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
