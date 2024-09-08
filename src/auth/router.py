from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import UserCreate, UserRead, UserLogin
from .controller import AuthController
from src.db.main import get_session

auth_router = APIRouter()


@auth_router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserRead)
async def register(user: UserCreate, session: AsyncSession = Depends(get_session)):
    return await AuthController.register(user, session)


@auth_router.post("/login", status_code=status.HTTP_200_OK, response_model=UserRead)
async def login(login_data: UserLogin, session: AsyncSession = Depends(get_session)):
    return await AuthController.login(login_data, session)
