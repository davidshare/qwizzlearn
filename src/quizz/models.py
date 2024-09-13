from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Column, UniqueConstraint
import sqlalchemy.dialects.postgresql as pg


class Quiz(SQLModel, table=True):
    __tablename__ = "quizzes"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(sa_column=Column(pg.INTEGER, nullable=False))
    title: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=False))
    description: Optional[str] = Field(default=None, sa_column=Column(pg.TEXT))
    slug: str = Field(sa_column=Column(
        pg.VARCHAR(255), unique=True, nullable=False))
    max_scores: Optional[int] = Field(
        default=None, sa_column=Column(pg.INTEGER, nullable=True))
    max_questions: Optional[int] = Field(
        default=None, sa_column=Column(pg.INTEGER, nullable=True))
    difficulty: int = Field(sa_column=Column(pg.INTEGER, nullable=False))
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


class QuizFeedback(SQLModel, table=True):
    __tablename__ = "quiz_feedback"

    id: Optional[int] = Field(default=None, primary_key=True)
    quiz_id: int = Field(sa_column=Column(pg.INTEGER, nullable=False))
    feedback_text: str = Field(sa_column=Column(pg.TEXT, nullable=False))
    min_score: float = Field(sa_column=Column(pg.FLOAT, nullable=False))
    max_score: float = Field(sa_column=Column(pg.FLOAT, nullable=False))

    # Relationships
    quiz: "Quiz" = Relationship(
        back_populates="feedback", sa_relationship_kwargs={"lazy": "selectin"})


class QuizSettings(SQLModel, table=True):
    __tablename__ = "quiz_settings"

    id: Optional[int] = Field(default=None, primary_key=True)
    quiz_id: int = Field(sa_column=Column(pg.INTEGER, nullable=False))
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
