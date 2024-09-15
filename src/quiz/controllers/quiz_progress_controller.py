from typing import List
from fastapi import Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
import logging

from src.db.main import get_session
from src.authentication.models import User
from ..services import QuizProgressService
from ..schemas import QuizProgressCreate, QuizProgressRead, QuizProgressUpdate

logger = logging.getLogger(__name__)

quiz_progress_service = QuizProgressService()


class QuizProgressController:
    @staticmethod
    async def create_quiz_progress(quiz_progress_data: QuizProgressCreate, user: User, session: AsyncSession = Depends(get_session)) -> QuizProgressRead:
        if not user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User ID is missing. You need a valid user to create quiz progress."
            )

        return await quiz_progress_service.create_quiz_progress(quiz_progress_data, user.id, session)

    @staticmethod
    async def get_quiz_progress_by_id(quiz_progress_id: int, session: AsyncSession = Depends(get_session)):
        quiz_progress = await quiz_progress_service.get_quiz_progress_by_id(quiz_progress_id, session)
        if not quiz_progress:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz progress not found"
            )
        return quiz_progress

    @staticmethod
    async def get_all_quiz_progresses(session: AsyncSession = Depends(get_session)):
        quiz_progresses = await quiz_progress_service.get_all_quiz_progresses(session)
        if not quiz_progresses:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No quiz progresses available"
            )
        return quiz_progresses

    @staticmethod
    async def update_quiz_progress(quiz_progress_id: int, quiz_progress_data: QuizProgressUpdate, session: AsyncSession = Depends(get_session)):
        quiz_progress = await quiz_progress_service.update_quiz_progress(quiz_progress_id, quiz_progress_data, session)
        if not quiz_progress:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz progress not found"
            )
        return quiz_progress

    @staticmethod
    async def delete_quiz_progress(quiz_progress_id: int, session: AsyncSession = Depends(get_session)):
        success = await quiz_progress_service.delete_quiz_progress(quiz_progress_id, session)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz progress not found"
            )
        return {"message": "Quiz progress deleted successfully"}
