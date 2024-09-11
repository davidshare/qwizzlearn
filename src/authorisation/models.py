from datetime import datetime
from typing import List, Optional

import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import Index
from sqlmodel import Column, Field, Relationship, SQLModel, UniqueConstraint


class UserRoles(SQLModel, table=True):
    """
    Association table between users and roles.

    Attributes:
        user_id (Optional[int]): Foreign key to the users table.
        role_id (Optional[int]): Foreign key to the roles table.
    """
    __tablename__ = "user_roles"

    user_id: Optional[int] = Field(
        default=None, foreign_key="users.id", primary_key=True)
    role_id: Optional[int] = Field(
        default=None, foreign_key="roles.id", primary_key=True)

    __table_args__ = (UniqueConstraint(
        'user_id', 'role_id', name='uq_user_role'),)


class RolePermissions(SQLModel, table=True):
    """
    Association table between roles and permissions.

    Attributes:
        role_id (Optional[int]): Foreign key to the roles table.
        permission_id (Optional[int]): Foreign key to the permissions table.
    """
    __tablename__ = "role_permissions"

    role_id: Optional[int] = Field(
        default=None, foreign_key="roles.id", primary_key=True)
    permission_id: Optional[int] = Field(
        default=None, foreign_key="permissions.id", primary_key=True)

    __table_args__ = (UniqueConstraint(
        'role_id', 'permission_id', name='uq_role_permission'),)


class Role(SQLModel, table=True):
    """
    Role model representing roles in the system.

    Attributes:
        id (Optional[int]): Primary key.
        name (str): Unique name of the role.
        description (Optional[str]): Description of the role.
        created_by (Optional[int]): ID of the user who created the role.
        created_at (datetime): Timestamp when the role was created.
        updated_at (datetime): Timestamp when the role was last updated.
        users (List["User"]): List of users associated with the role.
        permissions (List["Permission"]): List of permissions associated with the role.
    """
    __tablename__ = "roles"
    __table_args__ = (
        Index('ix_unique_role_name', 'name', unique=True),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(
        pg.VARCHAR, unique=True, nullable=False))
    description: Optional[str] = None
    created_by: Optional[int] = Field(default=None, foreign_key="users.id")

    # Use Python's datetime.now() for default values
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    users: List["User"] = Relationship(
        back_populates="roles", link_model=UserRoles)
    permissions: List["Permission"] = Relationship(
        back_populates="roles", link_model=RolePermissions)


class Permission(SQLModel, table=True):
    """
    Permission model representing actions that can be assigned to roles.

    Attributes:
        id (Optional[int]): Primary key.
        name (str): Unique name of the permission.
        action (str): Unique action that the permission allows.
        is_owner_only (bool): Whether the permission is restricted to the owner only.
        description (Optional[str]): Description of the permission.
        created_by (Optional[int]): ID of the user who created the permission.
        created_at (datetime): Timestamp when the permission was created.
        updated_at (datetime): Timestamp when the permission was last updated.
        roles (List["Role"]): List of roles associated with the permission.
    """
    __tablename__ = "permissions"
    __table_args__ = (
        Index('ix_unique_permission_name', 'name', unique=True),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(
        pg.VARCHAR, unique=True, nullable=False))
    action: str = Field(sa_column=Column(pg.VARCHAR, unique=True, index=True))
    is_owner_only: bool = Field(default=False)
    description: Optional[str] = None
    created_by: Optional[int] = Field(default=None, foreign_key="users.id")

    # Use Python's datetime.now() for default values
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    roles: List["Role"] = Relationship(
        back_populates="permissions", link_model=RolePermissions)
