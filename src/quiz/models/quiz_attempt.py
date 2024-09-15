from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Column, UniqueConstraint
import sqlalchemy.dialects.postgresql as pg
from .quiz_progress import QuizProgress

if TYPE_CHECKING:
    from src.questions.models.question_time_tracking import QuestionTimeTracking


class QuizAttempt(SQLModel, table=True):
    __tablename__ = "quiz_attempts"

    id: Optional[int] = Field(default=None, primary_key=True)
    quiz_id: Optional[int] = Field(default=None, foreign_key="quizzes.id")
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    attempt_number: int = Field(sa_column=Column(pg.INTEGER, nullable=False))
    score: float = Field(sa_column=Column(pg.FLOAT, nullable=False))
    started_at: datetime = Field(
        default_factory=datetime.now, sa_column=Column(pg.TIMESTAMP, nullable=False))
    finished_at: Optional[datetime] = Field(
        default=None, sa_column=Column(pg.TIMESTAMP))
    completed: bool = Field(
        default=False, sa_column=Column(pg.BOOLEAN, nullable=False))
    created_at: datetime = Field(
        default_factory=datetime.now, sa_column=Column(pg.TIMESTAMP, nullable=False))

    __table_args__ = (UniqueConstraint("user_id", "quiz_id",
                                       "attempt_number", name="uq_quiz_attempt_user_quiz"),)

    # Relationships
    quiz: "Quiz" = Relationship(
        back_populates="attempts", sa_relationship_kwargs={"lazy": "selectin"})
    quiz_progress_entries: List[QuizProgress] = Relationship(
        back_populates="quiz_attempt", sa_relationship_kwargs={"lazy": "selectin"})
    question_time_trackings: List["QuestionTimeTracking"] = Relationship(
        back_populates="quiz_attempt", sa_relationship_kwargs={"lazy": "selectin"}
    )
