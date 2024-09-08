from datetime import datetime, timedelta
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi import Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from .schemas import UserCreate, UserRead, UserLogin
from .service import AuthService
from .utils import verify_password, create_access_token
from .dependencies import RefreshTokenBearer

REFRESH_TOKEN_EXPIRY = 2
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

    @staticmethod
    async def login(login_data: UserLogin, session: AsyncSession = Depends(get_session)) -> UserRead:
        email = login_data.email
        password = login_data.password
        user = await user_service.get_user_by_email(email, session)

        if user is not None:
            valid_pass = verify_password(password, user.password_hash)

            if valid_pass:
                accesss_token = create_access_token(
                    user_data={
                        'email': user.email,
                        'id': user.id
                    }
                )

                refresh_token = create_access_token(
                    user_data={
                        'email': user.email,
                        'id': user.id
                    },
                    refresh=True,
                    expiry=timedelta(days=REFRESH_TOKEN_EXPIRY))

                return JSONResponse(
                    {
                        "message": "Login Successful",
                        "accesss_token": accesss_token,
                        "refresh_token": refresh_token,
                        "user": {
                            "email": user.email,
                            "id": user.id
                        }
                    }
                )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid email or password."
        )

    @staticmethod
    def refresh_token(token_details: dict = Depends(RefreshTokenBearer())):
        expiry_timestamp = token_details["exp"]

        if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
            new_access_token = create_access_token(user_data=token_details["user"])

            return JSONResponse(content={"access_token": new_access_token})
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )
