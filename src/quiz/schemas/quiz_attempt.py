from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class QuizAttemptBase(BaseModel):
    quiz_id: int = Field(ge=1)
    attempt_number: int = Field(ge=1)
    score: float = Field(ge=0)
    started_at: datetime
    finished_at: datetime
    completed: bool


class QuizAttemptCreate(QuizAttemptBase):
    pass


class QuizAttemptRead(QuizAttemptBase):
    user_id: int
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class QuizAttemptUpdate(BaseModel):
    score: Optional[float]
    finished_at: Optional[datetime]
    completed: Optional[bool]
