from datetime import datetime, timedelta
from uuid import uuid4
from jose import jwt, JWTError
from app.core.config import config
from app.core.exceptions import InternalServerException, UnauthorizedException
from app.core.security import hash_password, verify_password
from ..models.session import Session as UserSession
from ..models.token import Token
from ..models.device import Device
from ..models.user import User
from ..repositories.user import UserRepository
from ..repositories.session import SessionRepository
from ..repositories.token import TokenRepository
from ..repositories.device import DeviceRepository
from ..schemas.login import LoginRequest, LoginResponse
from ..schemas.token import TokenResponse
from ..schemas.user import UserCreate, UserResponse


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        session_repository: SessionRepository,
        token_repository: TokenRepository,
        device_repository: DeviceRepository,
    ):
        self.user_repository = user_repository
        self.session_repository = session_repository
        self.token_repository = token_repository
        self.device_repository = device_repository

    async def register_user(self, user_data: UserCreate) -> UserResponse:
        try:
            hashed_password = hash_password(user_data.password)
            user = User(
                username=user_data.username,
                email=user_data.email,
                phone_number=user_data.phone_number,
                password_hash=hashed_password,
            )
            created_user = await self.user_repository.create_user(user)
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
            device_info=device_info,
        )
        return await self.session_repository.create_session(session)

    async def create_device(self, user_id: int, device_info: str) -> Device:
        device = await self.device_repository.get_device_by_id(device_info)
        if device:
            return device
        device = Device(
            user_id=user_id,
            device_id=device_info,
            device_type="web",  # Default device type
            is_trusted=False,   # Mark as untrusted by default
        )
        return await self.device_repository.create_device(device)

    async def login(self, login_data: LoginRequest, device_info: str) -> LoginResponse:
        user = await self.authenticate_user(login_data.username, login_data.password)
        session = await self.create_session(user.id, device_info)
        token = await self.create_refresh_token(user.id, data={"sub": user.id})
        await self.create_device(user.id, device_info)
        access_token = self.create_access_token(data={"sub": user.id})
        return LoginResponse(
            access_token=access_token,
            refresh_token=token.refresh_token,
            token_type="bearer",
        )

    def create_access_token(self, data: dict) -> dict:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)
        return encoded_jwt

    async def create_refresh_token(self, user_id: int,  data: dict) -> Token:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=config.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)
        token = Token(
            user_id=user_id,
            refresh_token=encoded_jwt,
            expires_at=expire,
        )
        return await self.token_repository.create_token(token)

    def decode_token(self, token: str):
        try:
            payload = jwt.decode(
                token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
            return payload
        except JWTError as e:
            raise UnauthorizedException('Invalid token') from e

    async def refresh_token(self, refresh_token: str) -> TokenResponse:
        # Retrieve the token from the database
        token = await self.token_repository.get_token_by_refresh_token(refresh_token)
        if not token or token.revoked or token.expires_at < datetime.utcnow():
            raise UnauthorizedException("Invalid or expired refresh token")

        access_token = self.create_access_token(data={"sub": token.user_id})
        new_token = await self.create_refresh_token(token.user_id, data={"sub": token.user_id})

        # Revoke the old refresh token
        await self.token_repository.revoke_token(token.refresh_token)

        return TokenResponse(
            access_token=access_token,
            refresh_token=new_token.refresh_token,
            token_type="bearer",
            issued_at=datetime.utcnow(),
            expires_at=new_token.expires_at,
        )
