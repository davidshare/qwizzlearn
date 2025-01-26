from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.core.exceptions import ValidationException, UnauthorizedException

from ...repositories.user import UserRepository
from ...repositories.session import SessionRepository
from ...repositories.device import DeviceRepository
from ...repositories.token import TokenRepository
from ...schemas.user import UserCreate, UserResponse
from ...services.auth import AuthService

from ...schemas.login import LoginRequest, LoginResponse
from ...schemas.token import TokenRefresh, TokenResponse

auth_router = APIRouter()


def get_auth_service(session: AsyncSession):
    user_repository = UserRepository(session)
    token_repository = TokenRepository(session)
    device_repository = DeviceRepository(session)
    session_repository = SessionRepository(session)
    auth_service = AuthService(
        user_repository, session_repository, token_repository, device_repository)
    return auth_service


@auth_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    auth_service = get_auth_service(session)

    try:
        return await auth_service.register_user(user_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise ValidationException(
            detail={
                "message": "Validation error",
                "errors": str(e),
                "documentation_url": "https://api.example.com/docs"
            }
        ) from e


@auth_router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(
    login_data: LoginRequest,
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    auth_service = get_auth_service(session)

    device_info = request.headers.get("User-Agent", "Unknown Device")

    try:
        return await auth_service.login(login_data, device_info)
    except UnauthorizedException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)) from e
    except Exception as e:
        raise ValidationException(
            detail={
                "message": "Validation error",
                "errors": str(e),
                "documentation_url": "https://api.example.com/docs"
            }
        ) from e


@auth_router.post("/refresh-token", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def refresh_token(
    token_data: TokenRefresh,
    session: AsyncSession = Depends(get_session)
):
    auth_service = get_auth_service(session)

    try:
        return await auth_service.refresh_token(token_data.refresh_token)
    except UnauthorizedException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)) from e
    except Exception as e:
        raise ValidationException(
            detail={
                "message": "Validation error",
                "errors": str(e),
                "documentation_url": "https://api.example.com/docs"
            }
        ) from e
