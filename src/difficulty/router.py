from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.authentication.dependencies import AccessTokenBearer
from src.db.main import get_session

from .controller import DifficultyController
from .schemas import DifficultyCreate, DifficultyRead, DifficultyUpdate

difficulty_router = APIRouter()
access_token_bearer = AccessTokenBearer()


@difficulty_router.post("/", dependencies=[Depends(access_token_bearer)], status_code=status.HTTP_201_CREATED, response_model=DifficultyRead)
async def create_difficulty(difficulty_data: DifficultyCreate, session: AsyncSession = Depends(get_session)):
    return await DifficultyController.create_difficulty(difficulty_data, session)


@difficulty_router.get("/", dependencies=[Depends(access_token_bearer)], status_code=status.HTTP_200_OK, response_model=List[DifficultyRead])
async def get_all_difficulties(session: AsyncSession = Depends(get_session)):
    return await DifficultyController.get_all_difficulties(session)


@difficulty_router.get("/{difficulty_id}", dependencies=[Depends(access_token_bearer)], status_code=status.HTTP_200_OK, response_model=DifficultyRead)
async def get_difficulty_by_id(difficulty_id: int, session: AsyncSession = Depends(get_session)):
    return await DifficultyController.get_difficulty_by_id(difficulty_id, session)


@difficulty_router.get("/{difficulty_name}/name", dependencies=[Depends(access_token_bearer)], status_code=status.HTTP_200_OK, response_model=DifficultyRead)
async def get_difficulty_by_name(difficulty_name: str, session: AsyncSession = Depends(get_session)):
    return await DifficultyController.get_difficulty_by_name(difficulty_name, session)


@difficulty_router.put("/{difficulty_id}", dependencies=[Depends(access_token_bearer)], status_code=status.HTTP_200_OK, response_model=DifficultyRead)
async def update_difficulty(difficulty_id: int, difficulty_data: DifficultyUpdate, session: AsyncSession = Depends(get_session)):
    return await DifficultyController.update_difficulty(difficulty_id, difficulty_data, session)


@difficulty_router.delete("/{difficulty_id}", dependencies=[Depends(access_token_bearer)], status_code=status.HTTP_204_NO_CONTENT)
async def delete_difficulty(difficulty_id: int, session: AsyncSession = Depends(get_session)):
    return await DifficultyController.delete_difficulty(difficulty_id, session)
