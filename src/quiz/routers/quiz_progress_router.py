from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.authentication.dependencies import AccessTokenBearer, get_current_user
from src.authorisation.dependencies import route_with_action, authorize
from src.db.main import get_session

from ..controllers import QuizProgressController
from ..schemas import QuizProgressCreate, QuizProgressRead, QuizProgressUpdate

quiz_progress_router = APIRouter()
access_token_bearer = AccessTokenBearer()


@route_with_action('create_quiz_progress')
@quiz_progress_router.post("/", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_201_CREATED, response_model=QuizProgressRead)
async def create_quiz_progress(quiz_progress_data: QuizProgressCreate, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await QuizProgressController.create_quiz_progress(quiz_progress_data, user, session)


@quiz_progress_router.get("/", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=List[QuizProgressRead])
@route_with_action('get_all_quiz_progresses')
async def get_all_quiz_progresses(session: AsyncSession = Depends(get_session)):
    return await QuizProgressController.get_all_quiz_progresses(session)


@quiz_progress_router.get("/{quiz_progress_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=QuizProgressRead)
@route_with_action('get_quiz_progress_by_id')
async def get_quiz_progress_by_id(quiz_progress_id: int, session: AsyncSession = Depends(get_session)):
    return await QuizProgressController.get_quiz_progress_by_id(quiz_progress_id, session)


@route_with_action('update_quiz_progress')
@quiz_progress_router.put("/{quiz_progress_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=QuizProgressRead)
async def update_quiz_progress(quiz_progress_id: int, quiz_progress_data: QuizProgressUpdate, session: AsyncSession = Depends(get_session)):
    return await QuizProgressController.update_quiz_progress(quiz_progress_id, quiz_progress_data, session)


@route_with_action('delete_quiz_progress')
@quiz_progress_router.delete("/{quiz_progress_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_204_NO_CONTENT)
async def delete_quiz_progress(quiz_progress_id: int, session: AsyncSession = Depends(get_session)):
    return await QuizProgressController.delete_quiz_progress(quiz_progress_id, session)
