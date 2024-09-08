from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.main import get_session
from .schemas import UserCreate, UserRead, UserLogin
from .controller import AuthController
from .dependencies import RefreshTokenBearer, AccessTokenBearer
from src.db.redis import add_jti_to_blocklist

auth_router = APIRouter()


@auth_router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserRead)
async def register(user: UserCreate, session: AsyncSession = Depends(get_session)):
    return await AuthController.register(user, session)


@auth_router.post("/login", status_code=status.HTTP_200_OK, response_model=UserRead)
async def login(login_data: UserLogin, session: AsyncSession = Depends(get_session)):
    return await AuthController.login(login_data, session)


@auth_router.get("/refresh-token")
async def refresh_token(token_details: dict = Depends(RefreshTokenBearer())):
    return AuthController.refresh_token(token_details)


@auth_router.get("/logout")
async def logout(token_details: dict = Depends(AccessTokenBearer())) -> None:
    jti = token_details["jti"]
    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={
            "message": "Logged out successfully!!!",
            "status": status.HTTP_200_OK
        }
    )
