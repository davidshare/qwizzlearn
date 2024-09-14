from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.postgresql as pg
from src.tags.models.quiz_tag_link import QuizTagLink


class Quiz(SQLModel, table=True):
    __tablename__ = "quizzes"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(
        default=None, foreign_key="users.id", primary_key=True)
    title: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=False))
    description: Optional[str] = Field(default=None, sa_column=Column(pg.TEXT))
    slug: str = Field(sa_column=Column(
        pg.VARCHAR(255), unique=True, nullable=False))
    max_scores: Optional[int] = Field(
        default=None, sa_column=Column(pg.INTEGER, nullable=True))
    max_questions: Optional[int] = Field(
        default=None, sa_column=Column(pg.INTEGER, nullable=True))
    difficulty: Optional[int] = Field(
        default=None, foreign_key="difficulties.id", primary_key=True)
    time_limit: Optional[int] = Field(
        default=None, sa_column=Column(pg.INTEGER, nullable=True))
    published: bool = Field(
        default=False, sa_column=Column(pg.BOOLEAN, nullable=False))
    published_at: datetime = Field(
        default_factory=datetime.now, sa_column=Column(pg.TIMESTAMP, nullable=False))
    created_at: datetime = Field(
        default_factory=datetime.now, sa_column=Column(pg.TIMESTAMP, nullable=False))
    updated_at: datetime = Field(default_factory=datetime.now, sa_column=Column(
        pg.TIMESTAMP, nullable=False, onupdate=datetime.now))

    # Relationships
    attempts: List["QuizAttempt"] = Relationship(
        back_populates="quiz", sa_relationship_kwargs={"lazy": "selectin"})
    feedback: List["QuizFeedback"] = Relationship(
        back_populates="quiz", sa_relationship_kwargs={"lazy": "selectin"})
    settings: Optional["QuizSettings"] = Relationship(
        back_populates="quiz", sa_relationship_kwargs={"lazy": "selectin"})
    reports: Optional["QuizReports"] = Relationship(
        back_populates="quiz", sa_relationship_kwargs={"lazy": "selectin"})
    schedules: List["QuizSchedule"] = Relationship(
        back_populates="quiz", sa_relationship_kwargs={"lazy": "selectin"})
    questions: List["QuizQuestion"] = Relationship(
        back_populates="quiz", sa_relationship_kwargs={"lazy": "selectin"})
    tags: List["Tag"] = Relationship(
        back_populates="quizzes", link_model=QuizTagLink)
