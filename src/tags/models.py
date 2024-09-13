from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg


class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(
        pg.VARCHAR(255), nullable=False, unique=True))
    description: Optional[str] = Field(default=None, sa_column=Column(pg.TEXT))
    created_by: int = Field(sa_column=Column(pg.INTEGER, nullable=False))
    created_at: datetime = Field(
        default_factory=datetime.now, sa_column=Column(pg.TIMESTAMP, nullable=False))
    updated_at: datetime = Field(default_factory=datetime.now, sa_column=Column(
        pg.TIMESTAMP, nullable=False, onupdate=datetime.now))
    is_active: bool = Field(
        default=True, sa_column=Column(pg.BOOLEAN, nullable=False))
