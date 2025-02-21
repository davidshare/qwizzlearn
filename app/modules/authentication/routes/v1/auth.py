from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import config
from app.core.database import get_session
from app.core.exceptions import ValidationException, UnauthorizedException

from ...repositories.user import UserRepository
from ...repositories.session import SessionRepository
from ...repositories.device import DeviceRepository
from ...repositories.token import TokenRepository
from ...schemas.user import UserCreate, UserResponse
from ...services.auth import AuthService

from ...schemas.login import LoginRequest, SuccessLoginResponse
from ...schemas.token import TokenRefresh, TokenResponse

auth_router = APIRouter()


def get_auth_service(session: AsyncSession):
    user_repository = UserRepository(session)
    token_repository = TokenRepository(session)
    device_repository = DeviceRepository(session)
    session_repository = SessionRepository(session)
    auth_service = AuthService(
        user_repository, session_repository, token_repository, device_repository
    )
    return auth_service


@auth_router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register_user(
    user_data: UserCreate, session: AsyncSession = Depends(get_session)
):
    auth_service = get_auth_service(session)

    try:
        return await auth_service.register_user(user_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise ValidationException(
            detail={
                "message": "Validation error",
                "errors": str(e),
                "documentation_url": "https://api.example.com/docs",
            }
        ) from e


@auth_router.post(
    "/login", response_model=SuccessLoginResponse, status_code=status.HTTP_200_OK
)
async def login(
    response: Response,
    login_data: LoginRequest,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    IS_PRODUCTION = config.ENV == "production"
    auth_service = get_auth_service(session)
    device_info = request.headers.get("User-Agent", "Unknown Device")

    try:
        tokens = await auth_service.login(login_data, device_info)

        # Set HTTP-only cookies in the response
        response.set_cookie(
            key="refresh_token",
            value=tokens.refresh_token,
            httponly=True,
            max_age=7 * 24 * 60 * 60,  # 7 days
            expires=7 * 24 * 60 * 60,  # 7 days
            secure=IS_PRODUCTION,  # Only set to True in production
            samesite="lax",
        )

        return {
            "success": True,
            "message": "Login successful",
            "access_token": tokens.access_token,
        }
    except UnauthorizedException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        ) from e
    except Exception as e:
        print(e)
        raise ValidationException(
            detail={
                "message": "Validation error",
                "errors": str(e),
                "documentation_url": "https://api.example.com/docs",
            }
        ) from e


@auth_router.post(
    "/refresh-token", response_model=TokenResponse, status_code=status.HTTP_200_OK
)
async def refresh_token(
    token_data: TokenRefresh, session: AsyncSession = Depends(get_session)
):
    auth_service = get_auth_service(session)

    try:
        return await auth_service.refresh_token(token_data.refresh_token)
    except UnauthorizedException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        ) from e
    except Exception as e:
        print(e)
        raise ValidationException(
            detail={
                "message": "Validation error",
                "errors": str(e),
                "documentation_url": "https://api.example.com/docs",
            }
        ) from e
