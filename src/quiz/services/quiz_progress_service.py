from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import func
from sqlmodel import select
from ..schemas import QuizProgressCreate, QuizProgressRead, QuizProgressUpdate
from ..models import QuizProgress


class QuizProgressService:
    async def create_quiz_progress(self, quiz_progress_data: QuizProgressCreate, user_id: int, session: AsyncSession) -> QuizProgressRead:
        new_quiz_progress = QuizProgress(
            **quiz_progress_data.model_dump(), user_id=user_id)
        session.add(new_quiz_progress)
        await session.commit()
        await session.refresh(new_quiz_progress)
        return new_quiz_progress

    async def get_quiz_progress_by_id(self, quiz_progress_id: int, session: AsyncSession) -> QuizProgressRead:
        statement = select(QuizProgress).where(
            QuizProgress.id == quiz_progress_id)
        result = await session.exec(statement)
        quiz_progress = result.first()
        return quiz_progress

    async def get_all_quiz_progresses(self, session: AsyncSession) -> list[QuizProgressRead]:
        statement = select(QuizProgress)
        quiz_progresses = await session.exec(statement)
        return quiz_progresses.all()

    async def update_quiz_progress(self, quiz_progress_id: int, quiz_progress_data: QuizProgressUpdate, session: AsyncSession) -> QuizProgressRead:
        statement = select(QuizProgress).where(
            QuizProgress.id == quiz_progress_id)
        result = await session.exec(statement)
        quiz_progress = result.first()

        if not quiz_progress:
            return None

        for key, value in quiz_progress_data.dict(exclude_unset=True).items():
            setattr(quiz_progress, key, value)

        session.add(quiz_progress)
        await session.commit()
        session.refresh(quiz_progress)
        return quiz_progress

    async def delete_quiz_progress(self, quiz_progress_id: int, session: AsyncSession) -> bool:
        statement = select(QuizProgress).where(
            QuizProgress.id == quiz_progress_id)
        result = await session.exec(statement)
        quiz_progress = result.first()

        if not quiz_progress:
            return False

        await session.delete(quiz_progress)
        await session.commit()
        return True
