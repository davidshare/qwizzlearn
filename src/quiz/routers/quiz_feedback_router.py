from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.authentication.dependencies import AccessTokenBearer, get_current_user
from src.authorisation.dependencies import route_with_action, authorize
from src.db.main import get_session

from ..controllers import QuizFeedbackController
from ..schemas import QuizFeedbackCreate, QuizFeedbackRead, QuizFeedbackUpdate

quiz_feedback_router = APIRouter()
access_token_bearer = AccessTokenBearer()


@route_with_action('create_quiz_feedback')
@quiz_feedback_router.post("/", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_201_CREATED, response_model=QuizFeedbackRead)
async def create_quiz_feedback(quiz_feedback_data: QuizFeedbackCreate, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await QuizFeedbackController.create_quiz_feedback(quiz_feedback_data, user, session)


@quiz_feedback_router.get("/", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=List[QuizFeedbackRead])
@route_with_action('get_all_quiz_feedbacks')
async def get_all_quiz_feedbacks(session: AsyncSession = Depends(get_session)):
    return await QuizFeedbackController.get_all_quiz_feedbacks(session)


@quiz_feedback_router.get("/{quiz_feedback_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=QuizFeedbackRead)
@route_with_action('get_quiz_feedback_by_id')
async def get_quiz_feedback_by_id(quiz_feedback_id: int, session: AsyncSession = Depends(get_session)):
    return await QuizFeedbackController.get_quiz_feedback_by_id(quiz_feedback_id, session)


@route_with_action('update_quiz_feedback')
@quiz_feedback_router.put("/{quiz_feedback_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=QuizFeedbackRead)
async def update_quiz_feedback(quiz_feedback_id: int, quiz_feedback_data: QuizFeedbackUpdate, session: AsyncSession = Depends(get_session)):
    return await QuizFeedbackController.update_quiz_feedback(quiz_feedback_id, quiz_feedback_data, session)


@route_with_action('delete_quiz_feedback')
@quiz_feedback_router.delete("/{quiz_feedback_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_204_NO_CONTENT)
async def delete_quiz_feedback(quiz_feedback_id: int, session: AsyncSession = Depends(get_session)):
    return await QuizFeedbackController.delete_quiz_feedback(quiz_feedback_id, session)
