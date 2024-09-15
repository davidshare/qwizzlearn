from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.authentication.dependencies import AccessTokenBearer, get_current_user
from src.authorisation.dependencies import route_with_action, authorize
from src.db.main import get_session

from ..controllers import QuizSettingsController
from ..schemas import QuizSettingsCreate, QuizSettingsRead, QuizSettingsUpdate

quiz_settings_router = APIRouter()
access_token_bearer = AccessTokenBearer()


@route_with_action('create_quiz_settings')
@quiz_settings_router.post("/", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_201_CREATED, response_model=QuizSettingsRead)
async def create_quiz_settings(quiz_settings_data: QuizSettingsCreate, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await QuizSettingsController.create_quiz_settings(quiz_settings_data, user, session)


@quiz_settings_router.get("/", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=List[QuizSettingsRead])
@route_with_action('get_all_quiz_settings')
async def get_all_quiz_settings(session: AsyncSession = Depends(get_session)):
    return await QuizSettingsController.get_all_quiz_settings(session)


@quiz_settings_router.get("/{quiz_settings_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=QuizSettingsRead)
@route_with_action('get_quiz_settings_by_id')
async def get_quiz_settings_by_id(quiz_settings_id: int, session: AsyncSession = Depends(get_session)):
    return await QuizSettingsController.get_quiz_settings_by_id(quiz_settings_id, session)


@route_with_action('update_quiz_settings')
@quiz_settings_router.put("/{quiz_settings_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=QuizSettingsRead)
async def update_quiz_settings(quiz_settings_id: int, quiz_settings_data: QuizSettingsUpdate, session: AsyncSession = Depends(get_session)):
    return await QuizSettingsController.update_quiz_settings(quiz_settings_id, quiz_settings_data, session)


@route_with_action('delete_quiz_settings')
@quiz_settings_router.delete("/{quiz_settings_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_204_NO_CONTENT)
async def delete_quiz_settings(quiz_settings_id: int, session: AsyncSession = Depends(get_session)):
    return await QuizSettingsController.delete_quiz_settings(quiz_settings_id, session)
