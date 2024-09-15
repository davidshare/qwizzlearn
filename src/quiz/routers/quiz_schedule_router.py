from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.authentication.dependencies import AccessTokenBearer, get_current_user
from src.authorisation.dependencies import route_with_action, authorize
from src.db.main import get_session

from ..controllers import QuizScheduleController
from ..schemas import QuizScheduleCreate, QuizScheduleRead, QuizScheduleUpdate

quiz_schedule_router = APIRouter()
access_token_bearer = AccessTokenBearer()


@route_with_action('create_quiz_schedule')
@quiz_schedule_router.post("/", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_201_CREATED, response_model=QuizScheduleRead)
async def create_quiz_schedule(quiz_schedule_data: QuizScheduleCreate, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await QuizScheduleController.create_quiz_schedule(quiz_schedule_data, user, session)


@quiz_schedule_router.get("/", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=List[QuizScheduleRead])
@route_with_action('get_all_quiz_schedules')
async def get_all_quiz_schedules(session: AsyncSession = Depends(get_session)):
    return await QuizScheduleController.get_all_quiz_schedules(session)


@quiz_schedule_router.get("/{quiz_schedule_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=QuizScheduleRead)
@route_with_action('get_quiz_schedule_by_id')
async def get_quiz_schedule_by_id(quiz_schedule_id: int, session: AsyncSession = Depends(get_session)):
    return await QuizScheduleController.get_quiz_schedule_by_id(quiz_schedule_id, session)


@route_with_action('update_quiz_schedule')
@quiz_schedule_router.put("/{quiz_schedule_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=QuizScheduleRead)
async def update_quiz_schedule(quiz_schedule_id: int, quiz_schedule_data: QuizScheduleUpdate, session: AsyncSession = Depends(get_session)):
    return await QuizScheduleController.update_quiz_schedule(quiz_schedule_id, quiz_schedule_data, session)


@route_with_action('delete_quiz_schedule')
@quiz_schedule_router.delete("/{quiz_schedule_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_204_NO_CONTENT)
async def delete_quiz_schedule(quiz_schedule_id: int, session: AsyncSession = Depends(get_session)):
    return await QuizScheduleController.delete_quiz_schedule(quiz_schedule_id, session)
