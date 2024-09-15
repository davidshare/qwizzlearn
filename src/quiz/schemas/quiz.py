from typing import Optional
from datetime import datetime
from pydantic import BaseModel


# Quiz Schemas
class QuizBase(BaseModel):
    title: str
    description: Optional[str] = None
    max_scores: Optional[int] = None
    max_questions: Optional[int] = None
    difficulty: int = None
    time_limit: Optional[int] = None


class QuizCreate(QuizBase):
    pass


class QuizRead(QuizBase):
    id: int
    user_id: int
    slug: str
    published: bool = False
    published_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class QuizUpdate(BaseModel):
    user_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    slug: Optional[str] = None
    max_scores: Optional[int] = None
    max_questions: Optional[int] = None
    difficulty: Optional[int] = None
    time_limit: Optional[int] = None
    published: Optional[bool] = None
    published_at: Optional[datetime] = None
