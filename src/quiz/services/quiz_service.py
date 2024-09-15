from typing import List
from sqlalchemy import func
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.utils import generate_url_slug

from ..models import Quiz
from ..schemas import QuizCreate, QuizRead, QuizUpdate

from src.difficulty.service import DifficultyService
difficulty_service = DifficultyService()


class QuizService:
    async def create_quiz(self, quizzes_data: QuizCreate, user_id: int, session: AsyncSession) -> List[QuizRead]:

        existing_quizzes = []
        new_quizzes = []

        for quiz in quizzes_data:
            result = await session.exec(
                select(Quiz).where(Quiz.title == quiz.title)
            )
            existing_quiz = result.first()

            if existing_quiz:
                existing_quizzes.append(existing_quiz)
            else:
                new_quiz = Quiz(
                    **quiz.model_dump(), user_id=user_id, slug=generate_url_slug(quiz.title))
                new_quizzes.append(new_quiz)

        # Add new quizzes to the session and commit
        if new_quizzes:
            session.add_all(new_quizzes)
            await session.commit()

            # Ensure all new quizzes are refreshed
            for quiz in new_quizzes:
                try:
                    # Verify the instance is still attached to the session
                    if not session.is_active:
                        print("Session is not active. Cannot refresh.")
                    else:
                        await session.refresh(quiz)
                except Exception as e:
                    print(f"Error refreshing quiz instance: {e}")

        # Return all quizzes (both existing and new)
        return existing_quizzes + new_quizzes

    async def get_quiz_by_title(self, title: str, session: AsyncSession) -> QuizRead:
        statement = select(Quiz).where(
            func.lower(Quiz.title) == func.lower(title))
        result = await session.exec(statement)
        quiz = result.first()
        return quiz

    async def get_quiz_by_id(self, quiz_id: int, session: AsyncSession) -> QuizRead:
        statement = select(Quiz).where(Quiz.id == quiz_id)
        result = await session.exec(statement)
        quiz = result.first()
        return quiz

    async def get_quiz_by_slug(self, slug: str, session: AsyncSession) -> QuizRead:
        statement = select(Quiz).where(Quiz.slug == slug)
        result = await session.exec(statement)
        quiz = result.first()
        return quiz

    async def get_all_quizzes(self, session: AsyncSession) -> list[QuizRead]:
        statement = select(Quiz)
        quizzes = await session.exec(statement)
        return quizzes.all()

    async def update_quiz(self, quiz_id: int, quiz_data: QuizUpdate, session: AsyncSession) -> QuizRead:
        statement = select(Quiz).where(Quiz.id == quiz_id)
        result = await session.exec(statement)
        quiz = result.first()

        if not quiz:
            return None

        for key, value in quiz_data.dict(exclude_unset=True).items():
            setattr(quiz, key, value)

        session.add(quiz)
        await session.commit()
        session.refresh(quiz)
        return quiz

    async def delete_quiz(self, quiz_id: int, session: AsyncSession) -> bool:
        statement = select(Quiz).where(Quiz.id == quiz_id)
        result = await session.exec(statement)
        quiz = result.first()

        if not quiz:
            return False

        await session.delete(quiz)
        await session.commit()
        return True
