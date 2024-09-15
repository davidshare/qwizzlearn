from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.authentication.dependencies import AccessTokenBearer, get_current_user
from src.authorisation.dependencies import route_with_action, authorize
from src.db.main import get_session

from ..controllers import QuizController
from ..schemas import QuizCreate, QuizRead, QuizUpdate

quiz_router = APIRouter()
access_token_bearer = AccessTokenBearer()


@route_with_action('create_quiz')
@quiz_router.post("/", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_201_CREATED, response_model=List[QuizRead])
async def create_quiz(quiz_data: List[QuizCreate], user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await QuizController.create_quiz(quiz_data, user, session)


@quiz_router.get("/", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=List[QuizRead])
@route_with_action('get_all_quizzes')
async def get_all_quizzes(session: AsyncSession = Depends(get_session)):
    return await QuizController.get_all_quizzes(session)


@quiz_router.get("/{quiz_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=QuizRead)
@route_with_action('get_quiz_by_id')
async def get_quiz_by_id(quiz_id: int, session: AsyncSession = Depends(get_session)):
    return await QuizController.get_quiz_by_id(quiz_id, session)


@quiz_router.get("/{slug}/slug", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=QuizRead)
@route_with_action('get_quiz_by_slug')
async def get_quiz_by_slug(slug: str, session: AsyncSession = Depends(get_session)):
    return await QuizController.get_quiz_by_slug(slug, session)


@route_with_action('get_quiz_by_title')
@quiz_router.get("/{quiz_title}/title", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=QuizRead)
async def get_quiz_by_title(quiz_title: str, session: AsyncSession = Depends(get_session)):
    return await QuizController.get_quiz_by_title(quiz_title, session)


@route_with_action('update_quiz')
@quiz_router.put("/{quiz_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=QuizRead)
async def update_quiz(quiz_id: int, quiz_data: QuizUpdate, session: AsyncSession = Depends(get_session)):
    return await QuizController.update_quiz(quiz_id, quiz_data, session)


@route_with_action('delete_quiz')
@quiz_router.delete("/{quiz_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_204_NO_CONTENT)
async def delete_quiz(quiz_id: int, session: AsyncSession = Depends(get_session)):
    return await QuizController.delete_quiz(quiz_id, session)
