from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from ..schemas import (QuizAttemptCreate, QuizAttemptRead, QuizAttemptUpdate)
from ..models import QuizAttempt
from ..exceptions import DuplicateQuizAttemptException


class QuizAttemptService:
    async def create_quiz_attempt(self, quiz_attempt_data: QuizAttemptCreate, user_id: int, session: AsyncSession) -> QuizAttemptRead:
        quiz_id = quiz_attempt_data.quiz_id
        attempt_number = quiz_attempt_data.attempt_number

        if await self.quiz_attempt_exists(quiz_id, user_id, attempt_number, session):
            raise DuplicateQuizAttemptException(
                "This quiz attempt has already been recorded")

        new_quiz_attempt = QuizAttempt(
            **quiz_attempt_data.model_dump(), user_id=user_id)
        session.add(new_quiz_attempt)
        await session.commit()

        try:
            if not session.is_active:
                print("Session is not active. Cannot refresh.")
            else:
                await session.refresh(new_quiz_attempt)
        except Exception as e:
            print(f"Error refreshing quiz instance: {e}")
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

    async def quiz_attempt_exists(self, quiz_id: int, user_id: int, attempt_number: int, session: AsyncSession):
        statement = select(QuizAttempt).where(
            QuizAttempt.quiz_id == quiz_id,
            QuizAttempt.user_id == user_id,
            QuizAttempt.attempt_number == attempt_number
        )
        result = await session.exec(statement)
        quiz_attempt = result.first()
        return quiz_attempt is not None

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
