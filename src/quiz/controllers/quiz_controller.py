from typing import List
from fastapi import Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
import logging

from src.db.main import get_session
from src.authentication.models import User
from ..services import QuizService
from ..schemas import QuizCreate, QuizRead, QuizUpdate
from ..validator import QuizValidator

logger = logging.getLogger(__name__)

quiz_service = QuizService()


class QuizController:
    @staticmethod
    async def create_quiz(quiz_data: List[QuizCreate], user: User, session: AsyncSession = Depends(get_session)) -> QuizRead:
        if not user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User ID is missing. You need a valid user to create a quiz."
            )

        await QuizValidator.difficulties_exist(quiz_data, session)

        return await quiz_service.create_quiz(quiz_data, user.id, session)

    @staticmethod
    async def get_quiz_by_id(quiz_id: int, session: AsyncSession = Depends(get_session)):
        quiz = await quiz_service.get_quiz_by_id(quiz_id, session)
        if not quiz:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz not found"
            )
        return quiz

    @staticmethod
    async def get_quiz_by_title(quiz_title: str, session: AsyncSession = Depends(get_session)):
        quiz = await quiz_service.get_quiz_by_title(quiz_title, session)
        if not quiz:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz not found"
            )
        return quiz

    @staticmethod
    async def get_quiz_by_slug(slug: str, session: AsyncSession = Depends(get_session)):
        quiz = await quiz_service.get_quiz_by_slug(slug, session)
        if not quiz:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz not found"
            )
        return quiz

    @staticmethod
    async def get_all_quizzes(session: AsyncSession = Depends(get_session)):
        quizzes = await quiz_service.get_all_quizzes(session)
        if not quizzes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No quizzes available"
            )
        return quizzes

    @staticmethod
    async def update_quiz(quiz_id: int, quiz_data: QuizUpdate, session: AsyncSession = Depends(get_session)):
        quiz = await quiz_service.update_quiz(quiz_id, quiz_data, session)
        if not quiz:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz not found"
            )
        return quiz

    @staticmethod
    async def delete_quiz(quiz_id: int, session: AsyncSession = Depends(get_session)):
        success = await quiz_service.delete_quiz(quiz_id, session)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz not found"
            )
        return {"message": "Quiz deleted successfully"}
