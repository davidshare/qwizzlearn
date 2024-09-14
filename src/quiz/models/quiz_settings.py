from typing import Optional
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.postgresql as pg

class QuizSettings(SQLModel, table=True):
    __tablename__ = "quiz_settings"

    id: Optional[int] = Field(default=None, primary_key=True)
    quiz_id: Optional[int] = Field(
        default=None, foreign_key="quizzes.id", primary_key=True)
    browser_security: str = Field(
        sa_column=Column(pg.VARCHAR(255), nullable=False))
    shuffle_questions: bool = Field(
        default=False, sa_column=Column(pg.BOOLEAN, nullable=False))
    shuffle_answers: bool = Field(
        default=False, sa_column=Column(pg.BOOLEAN, nullable=False))
    max_attempts: Optional[int] = Field(
        default=None, sa_column=Column(pg.INTEGER, nullable=True))
    time_limit: Optional[int] = Field(
        default=None, sa_column=Column(pg.INTEGER, nullable=True))

    # Relationships
    quiz: "Quiz" = Relationship(
        back_populates="settings", sa_relationship_kwargs={"lazy": "selectin"})
