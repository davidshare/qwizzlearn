from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
import logging

from src.db.main import get_session
from .service import DifficultyService
from .schemas import DifficultyCreate, DifficultyRead

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
