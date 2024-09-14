from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg

from .question_tag_link import QuestionTagLink
from .quiz_tag_link import QuizTagLink

if TYPE_CHECKING:
    from src.questions.models.question import Question
    from src.quiz.models.quiz import Quiz


class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(
        pg.VARCHAR(255), nullable=False, unique=True))
    description: Optional[str] = Field(default=None, sa_column=Column(pg.TEXT))
    created_by: Optional[int] = Field(
        default=None, foreign_key="users.id", primary_key=True)
    created_at: datetime = Field(
        default_factory=datetime.now, sa_column=Column(pg.TIMESTAMP, nullable=False))
    updated_at: datetime = Field(default_factory=datetime.now, sa_column=Column(
        pg.TIMESTAMP, nullable=False, onupdate=datetime.now))
    is_active: bool = Field(
        default=True, sa_column=Column(pg.BOOLEAN, nullable=False))

    questions: List["Question"] = Relationship(
        back_populates="tags", link_model=QuestionTagLink
    )
    quizzes: List["Quiz"] = Relationship(
        back_populates="tags", link_model=QuizTagLink
    )
