from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.authentication.dependencies import AccessTokenBearer, get_current_user
from src.authorisation.dependencies import route_with_action, authorize
from src.db.main import get_session

from ..controllers.quiz_attempt_controller import QuizAttemptController
from ..schemas import QuizAttemptCreate, QuizAttemptRead, QuizAttemptUpdate

quiz_attempt_router = APIRouter()
access_token_bearer = AccessTokenBearer()


@route_with_action('create_quiz_attempt')
@quiz_attempt_router.post("/", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_201_CREATED, response_model=QuizAttemptRead)
async def create_quiz_attempt(quiz_attempt_data: QuizAttemptCreate, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await QuizAttemptController.create_quiz_attempt(quiz_attempt_data, user, session)


@quiz_attempt_router.get("/", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=List[QuizAttemptRead])
@route_with_action('get_all_quiz_attempts')
async def get_all_quiz_attempts(session: AsyncSession = Depends(get_session)):
    return await QuizAttemptController.get_all_quiz_attempts(session)


@quiz_attempt_router.get("/{quiz_attempt_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=QuizAttemptRead)
@route_with_action('get_quiz_attempt_by_id')
async def get_quiz_attempt_by_id(quiz_attempt_id: int, session: AsyncSession = Depends(get_session)):
    return await QuizAttemptController.get_quiz_attempt_by_id(quiz_attempt_id, session)

@route_with_action('delete_quiz_attempt')
@quiz_attempt_router.delete("/{quiz_attempt_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_204_NO_CONTENT)
async def delete_quiz_attempt(quiz_attempt_id: int, session: AsyncSession = Depends(get_session)):
    return await QuizAttemptController.delete_quiz_attempt(quiz_attempt_id, session)
