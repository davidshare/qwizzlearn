from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.postgresql as pg

class QuizReports(SQLModel, table=True):
    __tablename__ = "quiz_reports"

    id: Optional[int] = Field(default=None, primary_key=True)
    quiz_id: int = Field(sa_column=Column(pg.INTEGER, nullable=False))
    average_score: float = Field(sa_column=Column(pg.FLOAT, nullable=False))
    median_score: float = Field(sa_column=Column(pg.FLOAT, nullable=False))
    standard_deviation: float = Field(
        sa_column=Column(pg.FLOAT, nullable=False))
    created_at: datetime = Field(
        default_factory=datetime.now, sa_column=Column(pg.TIMESTAMP, nullable=False))

    # Relationships
    quiz: "Quiz" = Relationship(
        back_populates="reports", sa_relationship_kwargs={"lazy": "selectin"})
