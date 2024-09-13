from typing import Optional
from datetime import datetime
from pydantic import BaseModel


# Quiz Schemas
class QuizBase(BaseModel):
    user_id: int
    title: str
    description: Optional[str]
    slug: str
    max_scores: Optional[int]
    max_questions: Optional[int]
    difficulty: int
    time_limit: Optional[int]
    published: bool
    published_at: Optional[datetime]


class QuizCreate(QuizBase):
    pass


class QuizRead(QuizBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class QuizUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    slug: Optional[str]
    max_scores: Optional[int]
    max_questions: Optional[int]
    difficulty: Optional[int]
    time_limit: Optional[int]
    published: Optional[bool]
    published_at: Optional[datetime]
