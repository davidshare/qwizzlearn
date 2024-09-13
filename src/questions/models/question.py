from typing import List, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.postgresql as pg


class Question(SQLModel, table=True):
    __tablename__ = "questions"

    id: Optional[int] = Field(default=None, primary_key=True)
    text: str = Field(sa_column=Column(pg.TEXT, nullable=False))
    # Type of question (e.g., multiple choice, true/false)
    type: str = Field(sa_column=Column(pg.VARCHAR(100), nullable=False))
    max_score: float = Field(sa_column=Column(
        pg.FLOAT, nullable=False))
    # Foreign key to the user who created the question
    created_by: int = Field(sa_column=Column(pg.INTEGER, nullable=False))
    created_at: datetime = Field(
        default_factory=datetime.now, sa_column=Column(pg.TIMESTAMP, nullable=False))
    updated_at: datetime = Field(default_factory=datetime.now, sa_column=Column(
        pg.TIMESTAMP, nullable=False, onupdate=datetime.now))

    category_id: int = Field(sa_column=Column(pg.INTEGER, nullable=False))
    category: "Category" = Relationship(back_populates="questions")

    difficulty_id: int = Field(sa_column=Column(pg.INTEGER, nullable=False))
    difficulty: "Difficulty" = Relationship(back_populates="questions")

    tags: List["Tag"] = Relationship(
        back_populates="questions", sa_relationship_kwargs={"lazy": "selectin"})
    quizzes: List["QuizQuestion"] = Relationship(back_populates="question")

    tags: List["Tag"] = Relationship(
        back_populates="questions", sa_relationship_kwargs={"lazy": "selectin"})
    quizzes: List["QuizQuestion"] = Relationship(back_populates="question")
    time_trackings: List["QuestionTimeTracking"] = Relationship(
        back_populates="question")
    progress_entries: List["QuizProgress"] = Relationship(
        back_populates="question")
