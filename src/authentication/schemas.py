from datetime import datetime
from pydantic import EmailStr, BaseModel, Field
from typing import Optional, List

# Schema for creating a new user


class UserCreate(BaseModel):
    username: str = Field(max_length=20)
    email: EmailStr = Field(max_length=40)
    phone: Optional[str] = None
    # Corrected typo from mine_length to min_length
    password: str = Field(min_length=8)


# Schema for user login
class UserLogin(BaseModel):
    email: EmailStr = Field(max_length=40)
    # Corrected typo from mine_length to min_length
    password: str = Field(min_length=8)


# Schema for reading user data (response)
class UserRead(BaseModel):
    id: int
    username: str
    email: str
    email_verified: bool
    phone: Optional[str] = None
    phone_verified: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Allows SQLModel/ORM compatibility for reading models

# Schema for updating a user's data


class UserUpdate(BaseModel):
    username: Optional[str] = Field(max_length=20)
    email: Optional[EmailStr] = Field(max_length=40)
    phone: Optional[str] = None
    # Only required if updating the password
    password: Optional[str] = Field(min_length=8)

    class Config:
        from_attributes = True
