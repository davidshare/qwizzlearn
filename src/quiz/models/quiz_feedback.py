from typing import Optional
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.postgresql as pg


class QuizFeedback(SQLModel, table=True):
    __tablename__ = "quiz_feedback"

    id: Optional[int] = Field(default=None, primary_key=True)
    quiz_id: Optional[int] = Field(
        default=None, foreign_key="quizzes.id", primary_key=True)
    feedback_text: str = Field(sa_column=Column(pg.TEXT, nullable=False))
    min_score: float = Field(sa_column=Column(pg.FLOAT, nullable=False))
    max_score: float = Field(sa_column=Column(pg.FLOAT, nullable=False))

    # Relationships
    quiz: "Quiz" = Relationship(
        back_populates="feedback", sa_relationship_kwargs={"lazy": "selectin"})
