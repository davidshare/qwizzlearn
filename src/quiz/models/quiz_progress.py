from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.postgresql as pg


class QuizProgress(SQLModel, table=True):
    __tablename__ = "quiz_progress"

    id: Optional[int] = Field(default=None, primary_key=True)
    quiz_attempt_id: int = Field(sa_column=Column(pg.INTEGER, nullable=False))
    question_id: int = Field(sa_column=Column(pg.INTEGER, nullable=False))
    time_spent: int = Field(sa_column=Column(
        pg.INTEGER, nullable=False))  # Time spent in seconds
    answered: bool = Field(sa_column=Column(pg.BOOLEAN, nullable=False))
    skipped: bool = Field(sa_column=Column(pg.BOOLEAN, nullable=False))
    created_at: datetime = Field(
        default_factory=datetime.now, sa_column=Column(pg.TIMESTAMP, nullable=False))

    quiz_attempt: "QuizAttempt" = Relationship(
        back_populates="quiz_progress_entries")
    question: "Question" = Relationship(back_populates="progress_entries")
