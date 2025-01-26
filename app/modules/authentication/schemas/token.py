from datetime import datetime
from pydantic import BaseModel


class TokenBase(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenCreate(BaseModel):
    user_id: int
    refresh_token: str
    expires_at: datetime


class TokenResponse(TokenBase):
    issued_at: datetime
    expires_at: datetime


class TokenRefresh(BaseModel):
    refresh_token: str
