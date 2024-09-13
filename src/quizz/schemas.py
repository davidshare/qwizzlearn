from typing import Optional
from datetime import datetime
from pydantic import BaseModel


# Quiz Schemas
class QuizBase(BaseModel):
    user_id: int
    title: str
    description: Optional[str]
    slug: str
    max_scores: Optional[int]
    max_questions: Optional[int]
    difficulty: int
    time_limit: Optional[int]
    published: bool
    published_at: Optional[datetime]


class QuizCreate(QuizBase):
    pass


class QuizRead(QuizBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class QuizUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    slug: Optional[str]
    max_scores: Optional[int]
    max_questions: Optional[int]
    difficulty: Optional[int]
    time_limit: Optional[int]
    published: Optional[bool]
    published_at: Optional[datetime]


# QuizAttempt Schemas
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
        orm_mode = True


class QuizAttemptUpdate(BaseModel):
    score: Optional[float]
    finished_at: Optional[datetime]
    completed: Optional[bool]


# QuizFeedback Schemas
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


# QuizSettings Schemas
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


# QuizReports Schemas
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
