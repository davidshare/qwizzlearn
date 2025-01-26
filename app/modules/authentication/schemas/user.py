import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, constr, field_validator


class UserBase(BaseModel):
    username: str
    email: EmailStr
    phone_number: Optional[str] = None


class UserCreate(UserBase):
    password: constr(min_length=8)

    @field_validator("username", "email", "phone_number")
    def check_empty_fields(cls, value, field):
        if not value:
            raise ValueError(f"{field.name} is required")
        return value

    @field_validator("password")
    def validate_password_strength(cls, value):
        # Password strength rules
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", value):
            raise ValueError(
                "Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", value):
            raise ValueError(
                "Password must contain at least one lowercase letter")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError(
                "Password must contain at least one special character")
        return value


class UserResponse(UserBase):
    id: int
    email_verified: bool
    phone_verified: bool
    created_at: datetime
    updated_at: datetime
    is_active: bool
    is_locked: bool
    mfa_enabled: bool
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True
