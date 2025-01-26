from datetime import datetime, timedelta
from uuid import uuid4

from sqlmodel.ext.asyncio.session import AsyncSession
from jose import jwt

from app.core.config import config
from app.core.exceptions import InternalServerException, UnauthorizedException
from app.core.security import hash_password, verify_password

from ..models.session import Session as UserSession
from ..models.token import Token
from ..models.user import User
from ..repositories.user import UserRepository
from ..schemas.login import LoginRequest, LoginResponse
from ..schemas.token import TokenResponse
from ..schemas.user import UserCreate, UserResponse


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register_user(self, user_data: UserCreate) -> UserResponse:
        try:
            # Hash the password
            hashed_password = hash_password(user_data.password)

            # Create the user object
            user = User(
                username=user_data.username,
                email=user_data.email,
                phone_number=user_data.phone_number,
                password_hash=hashed_password,
            )

            # Save the user to the database asynchronously
            created_user = await self.user_repository.create_user(user)

            # Return the user response
            return UserResponse.model_validate(created_user)
        except Exception as e:
            raise InternalServerException(
                f"An error occurred: {str(e)}") from e

    async def authenticate_user(self, username: str, password: str) -> User:
        user = await self.user_repository.get_user_by_username(username)
        if not user or not verify_password(password, user.password_hash):
            raise UnauthorizedException("Incorrect username or password")
        return user

    async def create_session(self, user_id: int, device_info: str) -> UserSession:
        session = UserSession(
            user_id=user_id,
            session_token=str(uuid4()),
            expires_at=datetime.utcnow() + timedelta(days=7),
            device_info=device_info
        )
        return session

    async def create_token(self, user_id: int) -> Token:
        token = Token(
            user_id=user_id,
            refresh_token=str(uuid4()),
            expires_at=datetime.utcnow() + timedelta(days=30)
        )
        return token

    async def login(self, login_data: LoginRequest, device_info: str) -> LoginResponse:
        user = await self.authenticate_user(login_data.username, login_data.password)

        session = await self.create_session(user.id, device_info)
        token = await self.create_token(user.id)

        access_token = self.create_access_token(user.id)

        return LoginResponse(
            access_token=access_token,
            refresh_token=token.refresh_token,
            token_type="bearer"
        )

    def create_access_token(self, user_id: id) -> str:
        expires_delta = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {"sub": str(
            user_id), "exp": datetime.utcnow() + expires_delta}
        encoded_jwt = jwt.encode(
            to_encode, config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)
        return encoded_jwt

    async def refresh_token(self, refresh_token: str) -> TokenResponse:
        token = await self.user_repository.get_token_by_refresh_token(refresh_token)
        if not token or token.revoked or token.expires_at < datetime.utcnow():
            raise UnauthorizedException("Invalid or expired refresh token")

        access_token = self.create_access_token(token.user_id)
        new_refresh_token = await self.create_token(token.user_id)

        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token.refresh_token,
            token_type="bearer",
            issued_at=datetime.utcnow(),
            expires_at=new_refresh_token.expires_at
        )
