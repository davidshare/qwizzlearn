
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
        from_attributes = True


class QuizFeedbackUpdate(BaseModel):
    quiz_id: Optional[int] = None
    feedback_text: Optional[str] = None
    min_score: Optional[float] = None
    max_score: Optional[float] = None
