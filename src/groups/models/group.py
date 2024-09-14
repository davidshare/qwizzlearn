from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.postgresql as pg
from src.quiz.models.quiz_schedule import QuizSchedule
from src.groups.models.group_user import GroupUser


class Group(SQLModel, table=True):
    __tablename__ = "groups"

    id: int = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=False))
    description: Optional[str] = Field(default=None, sa_column=Column(pg.TEXT))
    created_by: int = Field(
        default=None, foreign_key="users.id")
    created_at: datetime = Field(
        default_factory=datetime.now, sa_column=Column(pg.TIMESTAMP, nullable=False))
    updated_at: datetime = Field(default_factory=datetime.now, sa_column=Column(
        pg.TIMESTAMP, nullable=False, onupdate=datetime.now))

    # Relationships
    users: List["User"] = Relationship(
        back_populates="groups", link_model=GroupUser, sa_relationship_kwargs={"lazy": "selectin"})
    quiz_schedules: List["QuizSchedule"] = Relationship(
        back_populates="group", sa_relationship_kwargs={"lazy": "selectin"})
