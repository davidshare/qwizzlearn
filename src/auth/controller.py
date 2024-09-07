
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from .schemas import UserCreate, UserRead
from .service import AuthService

user_service = AuthService()


class AuthController:
    @staticmethod
    async def register(user: UserCreate, session: AsyncSession = Depends(get_session)) -> UserRead:
        # Check if user with the given email or username exists
        existence = await user_service.user_exist(session, email=user.email, username=user.username)

        if existence.get('email'):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="User with this email already exists"
            )

        if existence.get('username'):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="User with this username already exists"
            )

        # Create new user if no existing user with the same email or username
        new_user = await user_service.create_user(user, session)
        return new_user
