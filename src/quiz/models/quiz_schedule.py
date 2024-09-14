from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.postgresql as pg


class QuizSchedule(SQLModel, table=True):
    __tablename__ = "quiz_schedule"

    id: Optional[int] = Field(default=None, primary_key=True)
    quiz_id: Optional[int] = Field(
        default=None, foreign_key="quizzes.id", primary_key=True)

    group_id: Optional[int] = Field(
        default=None, foreign_key="groups.id", primary_key=True)
    start_time: datetime = Field(
        default_factory=datetime.now, sa_column=Column(pg.TIMESTAMP, nullable=False))
    end_time: datetime = Field(default=None, sa_column=Column(pg.TIMESTAMP))

    quiz: "Quiz" = Relationship(back_populates="schedules")
    group: Optional["Group"] = Relationship(back_populates="quiz_schedules")
