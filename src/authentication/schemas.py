from datetime import datetime
from typing import Optional

from pydantic import EmailStr, BaseModel, Field

from src.authorisation.schemas import UserRolesResponse

# Schema for creating a new user


class UserCreate(BaseModel):
    """
    Schema for creating a new user.

    Attributes:
        username (str): The desired username for the new user. Must be between 1 and 20 characters.
        email (EmailStr): The email address of the new user. valid email up to 40 characters.
        phone (Optional[str]): The phone number of the new user. Optional field.
        password (str): The password for the new user. Must be at least 8 characters long.
    """
    username: str = Field(..., max_length=20)
    email: EmailStr = Field(..., max_length=40)
    phone: Optional[str] = None
    password: str = Field(..., min_length=8)
    role: Optional[UserRolesResponse] = []

# Schema for user login


class UserLogin(BaseModel):
    """
    Schema for user login.

    Attributes:
        email (EmailStr): email address
        password (str): password, must be at least 8 characters.
    """
    email: EmailStr = Field(..., max_length=40)
    password: str = Field(..., min_length=8)

# Schema for reading user data (response)


class UserRead(BaseModel):
    """
    Schema for reading user data.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        email_verified (bool): Whether the user's email has been verified.
        phone (Optional[str]): The phone number of the user, if available.
        phone_verified (bool): Whether the user's phone number has been verified.
        is_active (bool): Whether the user's account is currently active.
        roles (Optional[List]): A list of roles associated with the user.
        created_at (datetime): Timestamp of when the user was created.
        updated_at (datetime): Timestamp of when the user was last updated.

    Config:
        from_attributes (bool): Allows compatibility for reading models from SQLModel/ORM models.
    """
    id: int
    username: str
    email: str
    email_verified: bool
    phone: Optional[str] = None
    phone_verified: bool
    is_active: bool
    roles: Optional[UserRolesResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        """
        map to orm models
        """
        from_attributes = True

# Schema for updating a user's data


class UserUpdate(BaseModel):
    """
    Schema for updating a user's data.

    Attributes:
        username (Optional[str]): optional username, must be between 1 and 20 characters if provided
        email (Optional[EmailStr]): optional email address
        phone (Optional[str]): The new phone number for the user. Optional field.
        password (Optional[str]): optional password

    Config:
        from_attributes (bool): Allows compatibility for reading models from SQLModel/ORM models.
    """
    username: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = Field(None, max_length=40)
    phone: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)

    class Config:
        """
        map to orm models
        """
        from_attributes = True
