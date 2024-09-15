from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.postgresql as pg


class QuizFeedback(SQLModel, table=True):
    __tablename__ = "quiz_feedback"

    id: Optional[int] = Field(default=None, primary_key=True)
    quiz_id: Optional[int] = Field(
        default=None, foreign_key="quizzes.id")
    feedback_text: str = Field(sa_column=Column(pg.TEXT, nullable=False))
    min_score: float = Field(sa_column=Column(pg.FLOAT, nullable=False))
    max_score: float = Field(sa_column=Column(pg.FLOAT, nullable=False))
    created_at: datetime = Field(sa_column=Column(
        pg.TIMESTAMP, default=datetime.now))

    # Relationships
    quiz: "Quiz" = Relationship(
        back_populates="feedback", sa_relationship_kwargs={"lazy": "selectin"})

# TODO: create a ratings table and link it to this model
# TODO: the feedback should be specific to a particular quiz. if the user returns to it, it should be updated.
#TODO: this can be extracted into a feedback module and then we can handle feedback for questions, and answers, or general.
