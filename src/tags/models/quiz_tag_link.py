from typing import Optional
from sqlmodel import SQLModel, Field


class QuizTagLink(SQLModel, table=True):
    __tablename__ = "quiz_tag_link"
    quiz_id: Optional[int] = Field(
        default=None, foreign_key="quizzes.id", primary_key=True)
    tag_id: Optional[int] = Field(
        default=None, foreign_key="tags.id", primary_key=True)
