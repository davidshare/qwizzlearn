from fastapi import Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
import logging

from src.db.main import get_session
from .service import DifficultyService
from .schemas import DifficultyCreate, DifficultyRead, DifficultyUpdate

logger = logging.getLogger(__name__)


difficulty_service = DifficultyService()


class DifficultyController:
    @staticmethod
    async def create_difficulty(difficulty_data: DifficultyCreate, session: AsyncSession = Depends(get_session)) -> DifficultyRead:
        name = difficulty_data.name
        difficulty = await difficulty_service.get_difficulty_by_name(
            name, session)
        if difficulty:
            logger.info("The difficulty: %s already exists", name)
            return difficulty

        new_difficulty = await difficulty_service.create_difficulty(
            difficulty_data, session)
        return new_difficulty

    @staticmethod
    async def get_difficulty_by_id(difficulty_id: int, session: AsyncSession):
        difficulty = await difficulty_service.get_difficulty_by_id(difficulty_id, session)
        if not difficulty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Difficulty not found"
            )
        return difficulty

    @staticmethod
    async def get_difficulty_by_name(difficulty_name: str, session: AsyncSession):
        difficulty = await difficulty_service.get_difficulty_by_name(difficulty_name, session)
        if not difficulty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Difficulty not found"
            )
        return difficulty

    @staticmethod
    async def get_all_difficulties(session: AsyncSession):
        difficulty = await difficulty_service.get_all_difficulties(session)
        if not difficulty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="There are no difficulties"
            )
        return difficulty

    @staticmethod
    async def update_difficulty(difficulty_id: int, difficulty_data: DifficultyUpdate, session: AsyncSession):
        difficulty = await difficulty_service.update_difficulty(difficulty_id, difficulty_data, session)
        if not difficulty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Difficulty not found"
            )
        return difficulty

    @staticmethod
    async def delete_difficulty(difficulty_id: int, session: AsyncSession):
        success = await difficulty_service.delete_difficulty(difficulty_id, session)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Difficulty not found"
            )
        return {"message": "Difficulty deleted successfully"}
