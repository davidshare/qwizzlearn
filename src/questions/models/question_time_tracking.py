from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.postgresql as pg

if TYPE_CHECKING:
    from src.quiz.models.quiz_attempt import QuizAttempt
    from .question import Question


class QuestionTimeTracking(SQLModel, table=True):
    __tablename__ = "question_time_tracking"

    id: Optional[int] = Field(default=None, primary_key=True)
    quiz_attempt_id: Optional[int] = Field(
        default=None, foreign_key="quiz_attempts.id")
    question_id: Optional[int] = Field(
        default=None, foreign_key="questions.id")
    start_time: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, nullable=False))
    end_time: datetime = Field(sa_column=Column(pg.TIMESTAMP, nullable=False))
    time_spent: int = Field(sa_column=Column(
        pg.INTEGER, nullable=False))  # Time spent in seconds

    quiz_attempt: "QuizAttempt" = Relationship(
        back_populates="question_time_trackings")
    question: "Question" = Relationship(back_populates="time_trackings")
