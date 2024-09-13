
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class QuizScheduleBase(BaseModel):
    quiz_id: int
    group_id: Optional[int]
    start_time: datetime
    end_time: Optional[datetime]


class QuizScheduleCreate(QuizScheduleBase):
    pass


class QuizScheduleRead(QuizScheduleBase):
    id: int


class QuizScheduleUpdate(BaseModel):
    quiz_id: Optional[int]
    group_id: Optional[int]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
