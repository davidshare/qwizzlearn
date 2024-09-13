from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class QuizSettingsBase(BaseModel):
    quiz_id: int
    browser_security: str
    shuffle_questions: bool
    shuffle_answers: bool
    max_attempts: Optional[int]
    time_limit: Optional[int]


class QuizSettingsCreate(QuizSettingsBase):
    pass


class QuizSettingsRead(QuizSettingsBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class QuizSettingsUpdate(BaseModel):
    browser_security: Optional[str]
    shuffle_questions: Optional[bool]
    shuffle_answers: Optional[bool]
    max_attempts: Optional[int]
    time_limit: Optional[int]
