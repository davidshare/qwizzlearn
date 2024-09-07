from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import UserCreate, UserRead
from .controller import AuthController
from src.db.main import get_session

auth_router = APIRouter()


@auth_router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserRead)
async def register(user: UserCreate, session: AsyncSession = Depends(get_session)):
    return await AuthController.register(user, session)
