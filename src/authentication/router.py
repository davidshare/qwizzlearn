from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.authorisation.dependencies import route_with_action
from src.db.main import get_session

from .controller import AuthController
from .dependencies import (
    AccessTokenBearer, RefreshTokenBearer, get_current_user)
from .schemas import UserCreate, UserLogin, UserRead

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


@auth_router.get("/me")
@route_with_action("get_current_user")
async def current_user(user=Depends(get_current_user)):
    return user


@auth_router.get("/logout")
async def logout(token_details: dict = Depends(AccessTokenBearer())):
    return await AuthController.logout(token_details)
