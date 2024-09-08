from datetime import datetime
from pydantic import EmailStr, BaseModel, Field
from typing import Optional


class UserCreate(BaseModel):
    username: str = Field(max_length=20)
    email: EmailStr = Field(max_length=40)
    phone: Optional[str] = None
    password: str = Field(mine_length=8)


class UserLogin(BaseModel):
    email: EmailStr = Field(max_length=40)
    password: str = Field(mine_length=8)


class UserRead(BaseModel):
    id: int
    username: str
    email: str
    email_verified: bool
    phone: Optional[str] = None
    phone_verified: bool
    is_active: bool
    role: str
    created_at: datetime
    updated_at: datetime
