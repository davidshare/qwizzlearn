from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import func
from sqlmodel import select
from ..schemas import QuizFeedbackCreate, QuizFeedbackRead, QuizFeedbackUpdate
from ..models import QuizFeedback


class QuizFeedbackService:
    async def create_quiz_feedback(self, quiz_feedback_data: QuizFeedbackCreate, user_id: int, session: AsyncSession) -> QuizFeedbackRead:
        new_quiz_feedback = QuizFeedback(
            **quiz_feedback_data.model_dump(), user_id=user_id)
        session.add(new_quiz_feedback)
        await session.commit()
        await session.refresh(new_quiz_feedback)
        return new_quiz_feedback

    async def get_quiz_feedback_by_id(self, quiz_feedback_id: int, session: AsyncSession) -> QuizFeedbackRead:
        statement = select(QuizFeedback).where(
            QuizFeedback.id == quiz_feedback_id)
        result = await session.exec(statement)
        quiz_feedback = result.first()
        return quiz_feedback

    async def get_all_quiz_feedbacks(self, session: AsyncSession) -> list[QuizFeedbackRead]:
        statement = select(QuizFeedback)
        quiz_feedbacks = await session.exec(statement)
        return quiz_feedbacks.all()

    async def update_quiz_feedback(self, quiz_feedback_id: int, quiz_feedback_data: QuizFeedbackUpdate, session: AsyncSession) -> QuizFeedbackRead:
        statement = select(QuizFeedback).where(
            QuizFeedback.id == quiz_feedback_id)
        result = await session.exec(statement)
        quiz_feedback = result.first()

        if not quiz_feedback:
            return None

        for key, value in quiz_feedback_data.dict(exclude_unset=True).items():
            setattr(quiz_feedback, key, value)

        session.add(quiz_feedback)
        await session.commit()
        session.refresh(quiz_feedback)
        return quiz_feedback

    async def delete_quiz_feedback(self, quiz_feedback_id: int, session: AsyncSession) -> bool:
        statement = select(QuizFeedback).where(
            QuizFeedback.id == quiz_feedback_id)
        result = await session.exec(statement)
        quiz_feedback = result.first()

        if not quiz_feedback:
            return False

        await session.delete(quiz_feedback)
        await session.commit()
        return True
