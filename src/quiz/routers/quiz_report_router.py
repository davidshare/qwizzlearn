from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.authentication.dependencies import AccessTokenBearer, get_current_user
from src.authorisation.dependencies import route_with_action, authorize
from src.db.main import get_session

from ..controllers import QuizReportController
from ..schemas import QuizReportCreate, QuizReportUpdate, QuizReportRead

quiz_report_router = APIRouter()
access_token_bearer = AccessTokenBearer()


@route_with_action('create_quiz_report')
@quiz_report_router.post("/", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_201_CREATED, response_model=QuizReportRead)
async def create_quiz_report(quiz_report_data: QuizReportCreate, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await QuizReportController.create_quiz_report(quiz_report_data, user, session)


@quiz_report_router.get("/", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=List[QuizReportRead])
@route_with_action('get_all_quiz_reports')
async def get_all_quiz_reports(session: AsyncSession = Depends(get_session)):
    return await QuizReportController.get_all_quiz_reports(session)


@quiz_report_router.get("/{quiz_report_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=QuizReportRead)
@route_with_action('get_quiz_report_by_id')
async def get_quiz_report_by_id(quiz_report_id: int, session: AsyncSession = Depends(get_session)):
    return await QuizReportController.get_quiz_report_by_id(quiz_report_id, session)


@route_with_action('update_quiz_report')
@quiz_report_router.put("/{quiz_report_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=QuizReportRead)
async def update_quiz_report(quiz_report_id: int, quiz_report_data: QuizReportUpdate, session: AsyncSession = Depends(get_session)):
    return await QuizReportController.update_quiz_report(quiz_report_id, quiz_report_data, session)


@route_with_action('delete_quiz_report')
@quiz_report_router.delete("/{quiz_report_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_204_NO_CONTENT)
async def delete_quiz_report(quiz_report_id: int, session: AsyncSession = Depends(get_session)):
    return await QuizReportController.delete_quiz_report(quiz_report_id, session)
