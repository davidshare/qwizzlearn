from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class QuizReportBase(BaseModel):
    quiz_id: int
    average_score: float
    median_score: float
    standard_deviation: float


class QuizReportCreate(QuizReportBase):
    pass


class QuizReportRead(QuizReportBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class QuizReportUpdate(BaseModel):
    average_score: Optional[float]
    median_score: Optional[float]
    standard_deviation: Optional[float]
