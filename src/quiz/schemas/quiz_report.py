from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class QuizReportsBase(BaseModel):
    quiz_id: int
    average_score: float
    median_score: float
    standard_deviation: float


class QuizReportsCreate(QuizReportsBase):
    pass


class QuizReportsRead(QuizReportsBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class QuizReportsUpdate(BaseModel):
    average_score: Optional[float]
    median_score: Optional[float]
    standard_deviation: Optional[float]
