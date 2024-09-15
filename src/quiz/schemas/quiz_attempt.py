from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class QuizAttemptBase(BaseModel):
    quiz_id: int
    user_id: int
    attempt_number: int
    score: Optional[float]
    started_at: datetime
    finished_at: Optional[datetime]
    completed: bool


class QuizAttemptCreate(QuizAttemptBase):
    pass


class QuizAttemptRead(QuizAttemptBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class QuizAttemptUpdate(BaseModel):
    score: Optional[float]
    finished_at: Optional[datetime]
    completed: Optional[bool]
