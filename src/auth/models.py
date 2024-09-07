from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import Index
import sqlalchemy.dialects.postgresql as pg


class User(SQLModel, table=True):
    __tablename__ = "users"
    __table_args__ = (
        Index('ix_unique_username', 'username', unique=True),
        Index('ix_unique_email', 'email', unique=True),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(sa_column=Column(
        pg.VARCHAR, unique=True, nullable=False))  # Not null
    email: str = Field(sa_column=Column(
        pg.VARCHAR, unique=True, nullable=False))  # Not null
    email_verified: bool = False
    phone: Optional[str] = None
    phone_verified: bool = False
    password_hash: str = Field(exclude=True)
    is_active: bool = False
    role: str = "user"
    created_at: datetime = Field(sa_column=Column(
        pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(
        pg.TIMESTAMP, default=datetime.now))

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"
