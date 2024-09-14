from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.postgresql as pg
from src.questions.models.question import Question


class QuizProgress(SQLModel, table=True):
    __tablename__ = "quiz_progress"

    id: Optional[int] = Field(default=None, primary_key=True)
    quiz_attempt_id: Optional[int] = Field(
        default=None, foreign_key="quiz_attempts.id", primary_key=True)
    question_id: Optional[int] = Field(
        default=None, foreign_key="questions.id", primary_key=True)
    time_spent: int = Field(sa_column=Column(
        pg.INTEGER, nullable=False))  # Time spent in seconds
    answered: bool = Field(sa_column=Column(pg.BOOLEAN, nullable=False))
    skipped: bool = Field(sa_column=Column(pg.BOOLEAN, nullable=False))
    created_at: datetime = Field(
        default_factory=datetime.now, sa_column=Column(pg.TIMESTAMP, nullable=False))

    quiz_attempt: "QuizAttempt" = Relationship(
        back_populates="quiz_progress_entries")
    question: "Question" = Relationship(back_populates="progress_entries")
