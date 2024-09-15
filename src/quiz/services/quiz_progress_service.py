from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..models import QuizProgress
from ..schemas import QuizProgressCreate, QuizProgressRead, QuizProgressUpdate
from .quiz_service import QuizService
from .quiz_attempt_service import QuizAttemptService
from ..exceptions import QuizNotFoundException, QuizAttemptNotFoundException

quiz_attempt_service = QuizAttemptService()
quiz_service = QuizService()


class QuizProgressService:
    """Handle all database operations for the quiz progress
    """

    async def create_quiz_progress(
            self,
            quiz_progress_data: QuizProgressCreate,
            user_id: int,
            session: AsyncSession
    ) -> QuizProgressRead:
        """Create a new record for quiz progress

        Args:
            quiz_progress_data (QuizProgressCreate): input data for quiz progress
            user_id (int): user creating the progress
            session (AsyncSession): session for storing data

        Raises:
            QuizAttemptNotFoundException: exception raised when quiz attempt is not found
            QuizNotFoundException: exception raised when the quiz is not found

        Returns:
            QuizProgressRead: the output of creating the quiz progress
        """

        if not await quiz_attempt_service.get_quiz_attempt_by_id(
            quiz_progress_data.quiz_attempt_id, session
        ):
            raise QuizAttemptNotFoundException(f"No quiz attempt with the id {
                quiz_progress_data.quiz_id} exists")

        # TODO: THIS SHOULD BE A QUESTION NOT A QUIZ. FIX IT AFTER CREATING THE QUESTION MODULE
        if not await quiz_service.get_quiz_by_id(quiz_progress_data.quiz_id, session):
            raise QuizNotFoundException(f"No quiz with the id {
                quiz_progress_data.quiz_id} exists")

        new_quiz_progress = QuizProgress(
            **quiz_progress_data.model_dump(), user_id=user_id)

        try:
            session.add(new_quiz_progress)
            await session.commit()
            await session.refresh(new_quiz_progress)
        except Exception as e:
            print(f"Error refreshing quiz progress instance: {e}")
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
