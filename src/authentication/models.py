from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Column, Relationship
from sqlalchemy import Index
import sqlalchemy.dialects.postgresql as pg

from src.authorisation.models import Role, UserRoles
from src.groups.models.group import Group
from src.groups.models.group_user import GroupUser


class User(SQLModel, table=True):
    """
    Represents a user in the system.

    This model maps to the "users" table in the database and includes attributes for user identification,
    authentication, and status. It also establishes a many-to-many relationship with roles through the
    UserRoles association model.

    Attributes:
        id (Optional[int]): Unique identifier for the user, auto-incremented primary key.
        username (str): Unique username for the user, which cannot be null.
        email (str): Unique email address for the user, which cannot be null.
        email_verified (bool): Indicates whether the user's email address has been verified. Default is False.
        phone (Optional[str]): Phone number of the user. Can be null.
        phone_verified (bool): Indicates whether the user's phone number has been verified. Default is False.
        password_hash (str): Hashed password for the user. This field is excluded from serialization.
        is_active (bool): Indicates whether the user account is active. Default is False.
        roles (List[Role]): List of roles associated with the user, managed through a many-to-many relationship.
        created_at (datetime): Timestamp of when the user record was created. Defaults to the current time.
        updated_at (datetime): Timestamp of when the user record was last updated. Defaults to the current time.
    """

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
    password_hash: str = Field(..., nullable=False)
    is_active: bool = False

    roles: List[Role] = Relationship(back_populates="users", link_model=UserRoles, sa_relationship_kwargs={
        'lazy': 'selectin'})
    groups: List["Group"] = Relationship(
        back_populates="users", link_model=GroupUser, sa_relationship_kwargs={"lazy": "selectin"})

    created_at: datetime = Field(sa_column=Column(
        pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(
        pg.TIMESTAMP, default=datetime.now))

    def __repr__(self):
        """
        Returns a string representation of the User instance.

        This representation includes the user's ID, username, and email address.

        Returns:
            str: A formatted string showing the user's ID, username, and email.
        """
        return f"User(id={self.id}, username={self.username}, email={self.email})"
