from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import func
from sqlmodel import select
from ..schemas import QuizReportCreate, QuizReportRead, QuizReportUpdate
from ..models import QuizReport


class QuizReportervice:
    async def create_quiz_report(self, quiz_report_data: QuizReportCreate, user_id: int, session: AsyncSession) -> QuizReportRead:
        new_quiz_report = QuizReport(
            **quiz_report_data.model_dump(), user_id=user_id)
        session.add(new_quiz_report)
        await session.commit()
        await session.refresh(new_quiz_report)
        return new_quiz_report

    async def get_quiz_report_by_id(self, quiz_report_id: int, session: AsyncSession) -> QuizReportRead:
        statement = select(QuizReport).where(QuizReport.id == quiz_report_id)
        result = await session.exec(statement)
        quiz_report = result.first()
        return quiz_report

    async def get_all_quiz_reports(self, session: AsyncSession) -> list[QuizReportRead]:
        statement = select(QuizReport)
        quiz_reports = await session.exec(statement)
        return quiz_reports.all()

    async def update_quiz_report(self, quiz_report_id: int, quiz_report_data: QuizReportUpdate, session: AsyncSession) -> QuizReportRead:
        statement = select(QuizReport).where(QuizReport.id == quiz_report_id)
        result = await session.exec(statement)
        quiz_report = result.first()

        if not quiz_report:
            return None

        for key, value in quiz_report_data.dict(exclude_unset=True).items():
            setattr(quiz_report, key, value)

        session.add(quiz_report)
        await session.commit()
        session.refresh(quiz_report)
        return quiz_report

    async def delete_quiz_report(self, quiz_report_id: int, session: AsyncSession) -> bool:
        statement = select(QuizReport).where(QuizReport.id == quiz_report_id)
        result = await session.exec(statement)
        quiz_report = result.first()

        if not quiz_report:
            return False

        await session.delete(quiz_report)
        await session.commit()
        return True
