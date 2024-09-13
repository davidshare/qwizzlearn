from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.authentication.dependencies import AccessTokenBearer
from src.authorisation.dependencies import route_with_action, authorize
from src.db.main import get_session

from .controller import DifficultyController
from .schemas import DifficultyCreate, DifficultyRead, DifficultyUpdate

difficulty_router = APIRouter()
access_token_bearer = AccessTokenBearer()


@route_with_action('create_difficulty')
@difficulty_router.post("/", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_201_CREATED, response_model=DifficultyRead)
async def create_difficulty(difficulty_data: DifficultyCreate, session: AsyncSession = Depends(get_session)):
    return await DifficultyController.create_difficulty(difficulty_data, session)


@difficulty_router.get("/", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=List[DifficultyRead])
@route_with_action('get_all_difficulties')
async def get_all_difficulties(session: AsyncSession = Depends(get_session)):
    return await DifficultyController.get_all_difficulties(session)


@difficulty_router.get("/{difficulty_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=DifficultyRead)
@route_with_action('get_difficulty_by_id')
async def get_difficulty_by_id(difficulty_id: int, session: AsyncSession = Depends(get_session)):
    return await DifficultyController.get_difficulty_by_id(difficulty_id, session)


@route_with_action('get_difficulty_by_name')
@difficulty_router.get("/{difficulty_name}/name", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=DifficultyRead)
async def get_difficulty_by_name(difficulty_name: str, session: AsyncSession = Depends(get_session)):
    return await DifficultyController.get_difficulty_by_name(difficulty_name, session)


@route_with_action('update_difficulty')
@difficulty_router.put("/{difficulty_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=DifficultyRead)
async def update_difficulty(difficulty_id: int, difficulty_data: DifficultyUpdate, session: AsyncSession = Depends(get_session)):
    return await DifficultyController.update_difficulty(difficulty_id, difficulty_data, session)


@route_with_action('delete_difficulty')
@difficulty_router.delete("/{difficulty_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_204_NO_CONTENT)
async def delete_difficulty(difficulty_id: int, session: AsyncSession = Depends(get_session)):
    return await DifficultyController.delete_difficulty(difficulty_id, session)
