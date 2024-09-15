from fastapi import Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
import logging

from src.db.main import get_session
from src.authentication.models import User
from ..services import QuizAttemptService
from ..schemas import QuizAttemptCreate, QuizAttemptRead, QuizAttemptUpdate
from ..services.quiz_service import QuizService
from ..exceptions import DuplicateQuizAttemptException


logger = logging.getLogger(__name__)
quiz_service = QuizService()

quiz_attempt_service = QuizAttemptService()


class QuizAttemptController:
    @staticmethod
    async def create_quiz_attempt(quiz_attempt_data: QuizAttemptCreate, user: User, session: AsyncSession = Depends(get_session)) -> QuizAttemptRead:
        if not user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User ID is missing. You need a valid user to create a quiz attempt."
            )

        if not await quiz_service.get_quiz_by_id(quiz_attempt_data.quiz_id, session):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The quiz with id {
                    quiz_attempt_data.quiz_id} does not exist"
            )

        try:
            return await quiz_attempt_service.create_quiz_attempt(quiz_attempt_data, user.id, session)
        except DuplicateQuizAttemptException as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Quiz attempt already exists"
            ) from exc

    @staticmethod
    async def get_quiz_attempt_by_id(quiz_attempt_id: int, session: AsyncSession = Depends(get_session)):
        quiz_attempt = await quiz_attempt_service.get_quiz_attempt_by_id(quiz_attempt_id, session)
        if not quiz_attempt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz attempt not found"
            )
        return quiz_attempt

    @staticmethod
    async def get_all_quiz_attempts(session: AsyncSession = Depends(get_session)):
        quiz_attempts = await quiz_attempt_service.get_all_quiz_attempts(session)
        if not quiz_attempts:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No quiz attempts available"
            )
        return quiz_attempts

    @staticmethod
    async def update_quiz_attempt(quiz_attempt_id: int, quiz_attempt_data: QuizAttemptUpdate, session: AsyncSession = Depends(get_session)):
        quiz_attempt = await quiz_attempt_service.update_quiz_attempt(quiz_attempt_id, quiz_attempt_data, session)
        if not quiz_attempt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz attempt not found"
            )
        return quiz_attempt

    @staticmethod
    async def delete_quiz_attempt(quiz_attempt_id: int, session: AsyncSession = Depends(get_session)):
        success = await quiz_attempt_service.delete_quiz_attempt(quiz_attempt_id, session)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz attempt not found"
            )
        return {"message": "Quiz attempt deleted successfully"}
