import logging

from fastapi import Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.authentication.models import User
from src.db.main import get_session

from ..exceptions import QuizNotFoundException
from ..schemas import QuizFeedbackCreate, QuizFeedbackRead, QuizFeedbackUpdate
from ..services import QuizFeedbackService

logger = logging.getLogger(__name__)

quiz_feedback_service = QuizFeedbackService()


class QuizFeedbackController:
    @staticmethod
    async def create_quiz_feedback(feedback_data: QuizFeedbackCreate, user: User, session: AsyncSession = Depends(get_session)) -> QuizFeedbackRead:
        if not user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User ID is missing. You need a valid user to create quiz feedback."
            )

        try:
            return await quiz_feedback_service.create_quiz_feedback(feedback_data, user.id, session)
        except QuizNotFoundException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The quizz with the id {
                    feedback_data.quiz_id} does not exist."
            ) from e

    @staticmethod
    async def get_quiz_feedback_by_id(quiz_feedback_id: int, session: AsyncSession = Depends(get_session)):
        quiz_feedback = await quiz_feedback_service.get_quiz_feedback_by_id(quiz_feedback_id, session)
        if not quiz_feedback:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz feedback not found"
            )
        return quiz_feedback

    @staticmethod
    async def get_all_quiz_feedbacks(session: AsyncSession = Depends(get_session)):
        quiz_feedbacks = await quiz_feedback_service.get_all_quiz_feedbacks(session)
        if not quiz_feedbacks:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No quiz feedbacks available"
            )
        return quiz_feedbacks

    @staticmethod
    async def update_quiz_feedback(quiz_feedback_id: int, quiz_feedback_data: QuizFeedbackUpdate, session: AsyncSession = Depends(get_session)):
        quiz_feedback = await quiz_feedback_service.update_quiz_feedback(quiz_feedback_id, quiz_feedback_data, session)
        if not quiz_feedback:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz feedback not found"
            )
        return quiz_feedback

    @staticmethod
    async def delete_quiz_feedback(quiz_feedback_id: int, session: AsyncSession = Depends(get_session)):
        success = await quiz_feedback_service.delete_quiz_feedback(quiz_feedback_id, session)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz feedback not found"
            )
        return {"message": "Quiz feedback deleted successfully"}
