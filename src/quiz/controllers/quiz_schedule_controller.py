from typing import List
from fastapi import Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
import logging

from src.db.main import get_session
from src.authentication.models import User
from ..services import QuizScheduleService
from ..schemas import QuizScheduleCreate, QuizScheduleRead, QuizScheduleUpdate

logger = logging.getLogger(__name__)

quiz_schedule_service = QuizScheduleService()


class QuizScheduleController:
    @staticmethod
    async def create_quiz_schedule(quiz_schedule_data: QuizScheduleCreate, user: User, session: AsyncSession = Depends(get_session)) -> QuizScheduleRead:
        if not user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User ID is missing. You need a valid user to create a quiz schedule."
            )

        return await quiz_schedule_service.create_quiz_schedule(quiz_schedule_data, user.id, session)

    @staticmethod
    async def get_quiz_schedule_by_id(quiz_schedule_id: int, session: AsyncSession = Depends(get_session)):
        quiz_schedule = await quiz_schedule_service.get_quiz_schedule_by_id(quiz_schedule_id, session)
        if not quiz_schedule:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz schedule not found"
            )
        return quiz_schedule

    @staticmethod
    async def get_all_quiz_schedules(session: AsyncSession = Depends(get_session)):
        quiz_schedules = await quiz_schedule_service.get_all_quiz_schedules(session)
        if not quiz_schedules:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No quiz schedules available"
            )
        return quiz_schedules

    @staticmethod
    async def update_quiz_schedule(quiz_schedule_id: int, quiz_schedule_data: QuizScheduleUpdate, session: AsyncSession = Depends(get_session)):
        quiz_schedule = await quiz_schedule_service.update_quiz_schedule(quiz_schedule_id, quiz_schedule_data, session)
        if not quiz_schedule:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz schedule not found"
            )
        return quiz_schedule

    @staticmethod
    async def delete_quiz_schedule(quiz_schedule_id: int, session: AsyncSession = Depends(get_session)):
        success = await quiz_schedule_service.delete_quiz_schedule(quiz_schedule_id, session)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz schedule not found"
            )
        return {"message": "Quiz schedule deleted successfully"}
