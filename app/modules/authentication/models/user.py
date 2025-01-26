from datetime import datetime
from typing import Optional, List

from sqlmodel import Field, SQLModel, Relationship
from app.core.mixins import TimestampMixin


class User(SQLModel, TimestampMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    phone_number: Optional[str] = Field(unique=True, default=None)
    email_verified: bool = Field(default=False)
    phone_verified: bool = Field(default=False)
    is_active: bool = Field(default=False)
    is_locked: bool = Field(default=False)
    mfa_secret_key: Optional[str] = Field(default=None)
    mfa_enabled: bool = Field(default=False)
    last_login: Optional[datetime] = Field(default=None)

    devices: List["Device"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "dynamic"})
    sessions: List["Session"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "dynamic"})
    tokens: List["Token"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "dynamic"})
