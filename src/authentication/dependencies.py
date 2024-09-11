from fastapi import Depends, Request, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Any, List

from src.db.main import get_session
from src.db.redis import token_in_blocklist

from .utils import decode_token
from .service import AuthService
from .models import User

auth_service = AuthService()


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        token = creds.credentials
        token_data = decode_token(token)

        if not self.token_valid(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "This token is invalid or expired.",
                    "resolution": "Please get a new token"
                }
            )

        if await token_in_blocklist(token_data["jti"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "This token is invalid or has been revoked",
                    "resolution": "Please get a new token"
                }
            )
        self.verify_token_data(token_data)

        return token_data

    def token_valid(self, token: str) -> bool:
        decoded_token = decode_token(token)
        return True if decoded_token is not None else False

    def verify_token_data(self, token):
        raise NotImplementedError(
            "Please Override this method in the child classes")


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token: dict) -> None:
        if token and token['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token"
            )


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token: dict) -> None:
        if token and not token['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a refresh token"
            )


async def get_current_user(token_details: dict = Depends(AccessTokenBearer()), session: AsyncSession = Depends(get_session)):
    user_email = token_details['user']['email']
    user = await auth_service.get_user_by_email(user_email, session)
    return user
