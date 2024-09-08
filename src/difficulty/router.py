from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from .schemas import DifficultyRead, DifficultyCreate
from .controller import DifficultyController

difficulty_router = APIRouter()


@difficulty_router.post("/", status_code=status.HTTP_201_CREATED, response_model=DifficultyRead)
async def create_difficulty(difficulty_data: DifficultyCreate, session: AsyncSession = Depends(get_session)):
    return await DifficultyController.create_difficulty(difficulty_data, session)
