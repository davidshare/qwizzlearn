from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class QuestionBase(BaseModel):
    text: str
    type: str
    max_score: float


class QuestionCreate(QuestionBase):
    category_id: int
    difficulty_id: int  # Reference to the difficulty table
    tags: List[int]  # List of tag IDs
    created_by: int


class QuestionRead(QuestionBase):
    id: int
    category_id: int
    difficulty_id: int  # Reference to difficulty
    created_by: int
    created_at: datetime
    updated_at: datetime
    tags: List[int]  # List of tag IDs


class QuestionUpdate(QuestionBase):
    category_id: Optional[int]
    difficulty_id: Optional[int]  # Optionally update difficulty
    tags: Optional[List[int]]  # Optionally update tags
