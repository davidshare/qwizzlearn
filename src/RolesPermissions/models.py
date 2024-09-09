from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Column, Relationship
from sqlalchemy import Index
import sqlalchemy.dialects.postgresql as pg


class Role(SQLModel, table=True):
    __tablename__ = "roles"
    __table_args__ = (
        Index('ix_unique_role_name', 'name', unique=True),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(
        pg.VARCHAR, unique=True, nullable=False))
    description: Optional[str] = None
    created_by: int  # Foreign key to track which user created the role
    created_at: datetime = Field(default_factory=datetime.now())
    updated_at: datetime = Field(default_factory=datetime.now())

    # Relationships
    permissions: List["Permission"] = Relationship(back_populates="role")


class Permission(SQLModel, table=True):
    __tablename__ = "permissions"
    __table_args__ = (
        Index('ix_unique_permission_name', 'name', unique=True),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(
        pg.VARCHAR, unique=True, nullable=False))
    description: Optional[str] = None
    created_by: int  # Foreign key to track which user created the permission
    created_at: datetime = Field(default_factory=datetime.now())
    updated_at: datetime = Field(default_factory=datetime.now())

    # Relationships
    role_id: Optional[int] = Field(default=None, foreign_key="roles.id")
    role: Optional[Role] = Relationship(back_populates="permissions")
