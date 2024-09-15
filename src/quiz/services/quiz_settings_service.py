from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import func
from sqlmodel import select
from ..schemas import (QuizSettingsCreate, QuizSettingsRead, QuizSettingsUpdate)
from ..models import QuizSettings


class QuizSettingsService:
    async def create_quiz_settings(self, quiz_settings_data: QuizSettingsCreate, user_id: int, session: AsyncSession) -> QuizSettingsRead:
        new_quiz_settings = QuizSettings(
            **quiz_settings_data.model_dump(), user_id=user_id)
        session.add(new_quiz_settings)
        await session.commit()
        await session.refresh(new_quiz_settings)
        return new_quiz_settings

    async def get_quiz_settings_by_id(self, quiz_settings_id: int, session: AsyncSession) -> QuizSettingsRead:
        statement = select(QuizSettings).where(
            QuizSettings.id == quiz_settings_id)
        result = await session.exec(statement)
        quiz_settings = result.first()
        return quiz_settings

    async def get_all_quiz_settings(self, session: AsyncSession) -> list[QuizSettingsRead]:
        statement = select(QuizSettings)
        quiz_settings = await session.exec(statement)
        return quiz_settings.all()

    async def update_quiz_settings(self, quiz_settings_id: int, quiz_settings_data: QuizSettingsUpdate, session: AsyncSession) -> QuizSettingsRead:
        statement = select(QuizSettings).where(
            QuizSettings.id == quiz_settings_id)
        result = await session.exec(statement)
        quiz_settings = result.first()

        if not quiz_settings:
            return None

        for key, value in quiz_settings_data.dict(exclude_unset=True).items():
            setattr(quiz_settings, key, value)

        session.add(quiz_settings)
        await session.commit()
        session.refresh(quiz_settings)
        return quiz_settings

    async def delete_quiz_settings(self, quiz_settings_id: int, session: AsyncSession) -> bool:
        statement = select(QuizSettings).where(
            QuizSettings.id == quiz_settings_id)
        result = await session.exec(statement)
        quiz_settings = result.first()

        if not quiz_settings:
            return False

        await session.delete(quiz_settings)
        await session.commit()
        return True
