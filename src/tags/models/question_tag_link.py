from typing import Optional
from sqlmodel import SQLModel, Field


class QuestionTagLink(SQLModel, table=True):
    __tablename__ = "question_tag_link"
    question_id: Optional[int] = Field(
        default=None, foreign_key="questions.id", primary_key=True)
    tag_id: Optional[int] = Field(
        default=None, foreign_key="tags.id", primary_key=True)
