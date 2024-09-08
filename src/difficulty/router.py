from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from .schemas import DifficultyRead, DifficultyCreate
from .controller import DifficultyController
from src.auth.dependencies import AccessTokenBearer

difficulty_router = APIRouter()
access_token_bearer = AccessTokenBearer()


@difficulty_router.post("/", status_code=status.HTTP_201_CREATED, response_model=DifficultyRead)
async def create_difficulty(difficulty_data: DifficultyCreate, session: AsyncSession = Depends(get_session), user_details=Depends(access_token_bearer)):
    return await DifficultyController.create_difficulty(difficulty_data, session)
