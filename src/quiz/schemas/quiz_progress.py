from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class QuizProgressBase(BaseModel):
    quiz_attempt_id: int
    question_id: int
    time_spent: int
    answered: bool
    skipped: bool


class QuizProgressCreate(QuizProgressBase):
    pass


class QuizProgressRead(QuizProgressBase):
    id: int
    created_at: datetime


class QuizProgressUpdate(BaseModel):
    quiz_attempt_id: Optional[int]
    question_id: Optional[int]
    time_spent: Optional[int]
    answered: Optional[bool]
    skipped: Optional[bool]
