from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.postgresql as pg


class GroupUser(SQLModel, table=True):
    __tablename__ = "group_users"

    id: Optional[int] = Field(default=None, primary_key=True)
    group_id: int = Field(
        default=None, foreign_key="groups.id", primary_key=True)

    user_id: int = Field(
        default=None, foreign_key="users.id", primary_key=True)

    role: str = Field(sa_column=Column(pg.VARCHAR(100), nullable=False))
    joined_at: datetime = Field(
        default_factory=datetime.now, sa_column=Column(pg.TIMESTAMP, nullable=False))
