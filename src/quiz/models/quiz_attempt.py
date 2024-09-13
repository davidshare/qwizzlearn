from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.postgresql as pg


class QuizAttempt(SQLModel, table=True):
    __tablename__ = "quiz_attempts"

    id: Optional[int] = Field(default=None, primary_key=True)
    quiz_id: int = Field(sa_column=Column(pg.INTEGER, nullable=False))
    user_id: int = Field(sa_column=Column(pg.INTEGER, nullable=False))
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

    # Relationships
    quiz: "Quiz" = Relationship(
        back_populates="attempts", sa_relationship_kwargs={"lazy": "selectin"})
