from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import func
from sqlmodel import select
from ..schemas import (QuizAttemptCreate, QuizAttemptRead, QuizAttemptUpdate)
from ..models import QuizAttempt


class QuizAttemptService:
    async def create_quiz_attempt(self, quiz_attempt_data: QuizAttemptCreate, user_id: int, session: AsyncSession) -> QuizAttemptRead:
        new_quiz_attempt = QuizAttempt(
            **quiz_attempt_data.model_dump(), user_id=user_id)
        session.add(new_quiz_attempt)
        await session.commit()
        await session.refresh(new_quiz_attempt)
        return new_quiz_attempt

    async def get_quiz_attempt_by_id(self, quiz_attempt_id: int, session: AsyncSession) -> QuizAttemptRead:
        statement = select(QuizAttempt).where(
            QuizAttempt.id == quiz_attempt_id)
        result = await session.exec(statement)
        quiz_attempt = result.first()
        return quiz_attempt

    async def get_all_quiz_attempts(self, session: AsyncSession) -> list[QuizAttemptRead]:
        statement = select(QuizAttempt)
        quiz_attempts = await session.exec(statement)
        return quiz_attempts.all()

    async def update_quiz_attempt(self, quiz_attempt_id: int, quiz_attempt_data: QuizAttemptUpdate, session: AsyncSession) -> QuizAttemptRead:
        statement = select(QuizAttempt).where(
            QuizAttempt.id == quiz_attempt_id)
        result = await session.exec(statement)
        quiz_attempt = result.first()

        if not quiz_attempt:
            return None

        for key, value in quiz_attempt_data.dict(exclude_unset=True).items():
            setattr(quiz_attempt, key, value)

        session.add(quiz_attempt)
        await session.commit()
        session.refresh(quiz_attempt)
        return quiz_attempt

    async def delete_quiz_attempt(self, quiz_attempt_id: int, session: AsyncSession) -> bool:
        statement = select(QuizAttempt).where(
            QuizAttempt.id == quiz_attempt_id)
        result = await session.exec(statement)
        quiz_attempt = result.first()

        if not quiz_attempt:
            return False

        await session.delete(quiz_attempt)
        await session.commit()
        return True
