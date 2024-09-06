from sqlmodel import SQLModel, Field, Column
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int = Field(default=None, primary_key=True)
    username: str
    email: str
    email_verified: bool = False
    phone: str
    phone_verified: bool = False
    password_hash: str
    is_active: bool = False
    role: str = "user"
    created_at: datetime = Field(sa_column=Column(
        pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(
        pg.TIMESTAMP, default=datetime.now))

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"
