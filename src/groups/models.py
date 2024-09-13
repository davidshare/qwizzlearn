from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.postgresql as pg


class Group(SQLModel, table=True):
    __tablename__ = "groups"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=False))
    description: Optional[str] = Field(default=None, sa_column=Column(pg.TEXT))
    created_by: int = Field(sa_column=Column(
        pg.INTEGER, nullable=False), foreign_key="users.id")
    created_at: datetime = Field(
        default_factory=datetime.now, sa_column=Column(pg.TIMESTAMP, nullable=False))
    updated_at: datetime = Field(default_factory=datetime.now, sa_column=Column(
        pg.TIMESTAMP, nullable=False, onupdate=datetime.now))

    # Relationships
    users: List["GroupUser"] = Relationship(
        back_populates="group", sa_relationship_kwargs={"lazy": "selectin"})


class GroupUser(SQLModel, table=True):
    __tablename__ = "group_users"

    id: Optional[int] = Field(default=None, primary_key=True)
    group_id: int = Field(sa_column=Column(
        pg.INTEGER, nullable=False), foreign_key="groups.id")
    user_id: int = Field(sa_column=Column(
        pg.INTEGER, nullable=False), foreign_key="users.id")
    role: str = Field(sa_column=Column(pg.VARCHAR(100), nullable=False))
    joined_at: datetime = Field(
        default_factory=datetime.now, sa_column=Column(pg.TIMESTAMP, nullable=False))

    # Relationships
    group: "Group" = Relationship(back_populates="users")
    user: "User" = Relationship(back_populates="groups")
