from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import func
from sqlmodel import select
from ..schemas import QuizScheduleCreate, QuizScheduleRead, QuizScheduleUpdate
from ..models import QuizSchedule


class QuizScheduleService:
    async def create_quiz_schedule(self, quiz_schedule_data: QuizScheduleCreate, user_id: int, session: AsyncSession) -> QuizScheduleRead:
        new_quiz_schedule = QuizSchedule(
            **quiz_schedule_data.model_dump(), user_id=user_id)
        session.add(new_quiz_schedule)
        await session.commit()
        await session.refresh(new_quiz_schedule)
        return new_quiz_schedule

    async def get_quiz_schedule_by_id(self, quiz_schedule_id: int, session: AsyncSession) -> QuizScheduleRead:
        statement = select(QuizSchedule).where(
            QuizSchedule.id == quiz_schedule_id)
        result = await session.exec(statement)
        quiz_schedule = result.first()
        return quiz_schedule

    async def get_all_quiz_schedules(self, session: AsyncSession) -> list[QuizScheduleRead]:
        statement = select(QuizSchedule)
        quiz_schedules = await session.exec(statement)
        return quiz_schedules.all()

    async def update_quiz_schedule(self, quiz_schedule_id: int, quiz_schedule_data: QuizScheduleUpdate, session: AsyncSession) -> QuizScheduleRead:
        statement = select(QuizSchedule).where(
            QuizSchedule.id == quiz_schedule_id)
        result = await session.exec(statement)
        quiz_schedule = result.first()

        if not quiz_schedule:
            return None

        for key, value in quiz_schedule_data.dict(exclude_unset=True).items():
            setattr(quiz_schedule, key, value)

        session.add(quiz_schedule)
        await session.commit()
        session.refresh(quiz_schedule)
        return quiz_schedule

    async def delete_quiz_schedule(self, quiz_schedule_id: int, session: AsyncSession) -> bool:
        statement = select(QuizSchedule).where(
            QuizSchedule.id == quiz_schedule_id)
        result = await session.exec(statement)
        quiz_schedule = result.first()

        if not quiz_schedule:
            return False

        await session.delete(quiz_schedule)
        await session.commit()
        return True
