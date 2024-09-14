from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class QuestionTimeTrackingBase(BaseModel):
    quiz_attempt_id: int
    question_id: int
    start_time: datetime
    end_time: datetime
    time_spent: int


class QuestionTimeTrackingCreate(QuestionTimeTrackingBase):
    pass


class QuestionTimeTrackingRead(QuestionTimeTrackingBase):
    id: int


class QuestionTimeTrackingUpdate(BaseModel):
    quiz_attempt_id: Optional[int]
    question_id: Optional[int]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    time_spent: Optional[int]
