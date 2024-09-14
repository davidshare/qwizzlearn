from typing import List, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.postgresql as pg
from src.categories.models import Category
from src.difficulty.models import Difficulty
from .quiz_question import QuizQuestion
from src.tags.models.question_tag_link import QuestionTagLink


class Question(SQLModel, table=True):
    __tablename__ = "questions"

    id: Optional[int] = Field(default=None, primary_key=True)
    text: str = Field(sa_column=Column(pg.TEXT, nullable=False))
    type: str = Field(sa_column=Column(pg.VARCHAR(100), nullable=False))
    max_score: float = Field(sa_column=Column(pg.FLOAT, nullable=False))
    created_by: Optional[int] = Field(
        default=None, foreign_key="users.id", primary_key=True)
    created_at: datetime = Field(
        default_factory=datetime.now, sa_column=Column(pg.TIMESTAMP, nullable=False))
    updated_at: datetime = Field(default_factory=datetime.now, sa_column=Column(
        pg.TIMESTAMP, nullable=False, onupdate=datetime.now))
    category_id: Optional[int] = Field(
        default=None, foreign_key="categories.id", primary_key=True)
    difficulty_id: Optional[int] = Field(
        default=None, foreign_key="difficulties.id", primary_key=True)

    category: "Category" = Relationship(back_populates="questions")
    difficulty: "Difficulty" = Relationship(back_populates="questions")

    quizzes: List["QuizQuestion"] = Relationship(back_populates="question")
    tags: List["Tag"] = Relationship(
        back_populates="questions", link_model=QuestionTagLink)
    time_trackings: List["QuestionTimeTracking"] = Relationship(
        back_populates="question")
    progress_entries: List["QuizProgress"] = Relationship(
        back_populates="question")