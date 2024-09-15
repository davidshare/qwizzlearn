from typing import List
from fastapi import Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
import logging

from src.db.main import get_session
from src.authentication.models import User
from ..services import QuizReportervice
from ..schemas import QuizReportCreate, QuizReportRead, QuizReportUpdate

logger = logging.getLogger(__name__)

quiz_reports_service = QuizReportervice()


class QuizReportController:
    @staticmethod
    async def create_quiz_report(quiz_report_data: QuizReportCreate, user: User, session: AsyncSession = Depends(get_session)) -> QuizReportRead:
        if not user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User ID is missing. You need a valid user to create a quiz report."
            )

        return await quiz_reports_service.create_quiz_report(quiz_report_data, user.id, session)

    @staticmethod
    async def get_quiz_report_by_id(quiz_report_id: int, session: AsyncSession = Depends(get_session)):
        quiz_report = await quiz_reports_service.get_quiz_report_by_id(quiz_report_id, session)
        if not quiz_report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz report not found"
            )
        return quiz_report

    @staticmethod
    async def get_all_quiz_reports(session: AsyncSession = Depends(get_session)):
        quiz_reports = await quiz_reports_service.get_all_quiz_reports(session)
        if not quiz_reports:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No quiz reports available"
            )
        return quiz_reports

    @staticmethod
    async def update_quiz_report(quiz_report_id: int, quiz_report_data: QuizReportUpdate, session: AsyncSession = Depends(get_session)):
        quiz_report = await quiz_reports_service.update_quiz_report(quiz_report_id, quiz_report_data, session)
        if not quiz_report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz report not found"
            )
        return quiz_report

    @staticmethod
    async def delete_quiz_report(quiz_report_id: int, session: AsyncSession = Depends(get_session)):
        success = await quiz_reports_service.delete_quiz_report(quiz_report_id, session)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz report not found"
            )
        return {"message": "Quiz report deleted successfully"}
