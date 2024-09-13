from pydantic import BaseModel
from typing import Optional


class QuizQuestionBase(BaseModel):
    quiz_id: int
    question_id: int


class QuizQuestionCreate(QuizQuestionBase):
    pass


class QuizQuestionRead(QuizQuestionBase):
    pass


class QuizQuestionUpdate(BaseModel):
    quiz_id: Optional[int] = None
    question_id: Optional[int] = None
