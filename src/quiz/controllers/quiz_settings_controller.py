from typing import List
from fastapi import Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
import logging

from src.db.main import get_session
from src.authentication.models import User
from ..services import QuizSettingsService
from ..schemas import QuizSettingsCreate, QuizSettingsRead, QuizSettingsUpdate

logger = logging.getLogger(__name__)

quiz_settings_service = QuizSettingsService()


class QuizSettingsController:
    @staticmethod
    async def create_quiz_settings(quiz_settings_data: QuizSettingsCreate, user: User, session: AsyncSession = Depends(get_session)) -> QuizSettingsRead:
        if not user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User ID is missing. You need a valid user to create quiz settings."
            )

        return await quiz_settings_service.create_quiz_settings(quiz_settings_data, user.id, session)

    @staticmethod
    async def get_quiz_settings_by_id(quiz_settings_id: int, session: AsyncSession = Depends(get_session)):
        quiz_settings = await quiz_settings_service.get_quiz_settings_by_id(quiz_settings_id, session)
        if not quiz_settings:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz settings not found"
            )
        return quiz_settings

    @staticmethod
    async def get_all_quiz_settings(session: AsyncSession = Depends(get_session)):
        quiz_settings = await quiz_settings_service.get_all_quiz_settings(session)
        if not quiz_settings:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No quiz settings available"
            )
        return quiz_settings

    @staticmethod
    async def update_quiz_settings(quiz_settings_id: int, quiz_settings_data: QuizSettingsUpdate, session: AsyncSession = Depends(get_session)):
        quiz_settings = await quiz_settings_service.update_quiz_settings(quiz_settings_id, quiz_settings_data, session)
        if not quiz_settings:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz settings not found"
            )
        return quiz_settings

    @staticmethod
    async def delete_quiz_settings(quiz_settings_id: int, session: AsyncSession = Depends(get_session)):
        success = await quiz_settings_service.delete_quiz_settings(quiz_settings_id, session)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz settings not found"
            )
        return {"message": "Quiz settings deleted successfully"}
