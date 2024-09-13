
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class QuizFeedbackBase(BaseModel):
    quiz_id: int
    feedback_text: str
    min_score: float
    max_score: float


class QuizFeedbackCreate(QuizFeedbackBase):
    pass


class QuizFeedbackRead(QuizFeedbackBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class QuizFeedbackUpdate(BaseModel):
    feedback_text: Optional[str]
    min_score: Optional[float]
    max_score: Optional[float]
