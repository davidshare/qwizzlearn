from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.authentication.dependencies import AccessTokenBearer, get_current_user
from src.authorisation.dependencies import route_with_action, authorize
from src.db.main import get_session

from .controller import TagController
from .schemas import TagCreate, TagRead, TagUpdate

tag_router = APIRouter()
access_token_bearer = AccessTokenBearer()


@route_with_action('create_tag')
@tag_router.post("/", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_201_CREATED, response_model=List[TagRead])
async def create_tag(tag_data: List[TagCreate], user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await TagController.create_tag(tag_data, user, session)


@tag_router.get("/", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=List[TagRead])
@route_with_action('get_all_tags')
async def get_all_tags(session: AsyncSession = Depends(get_session)):
    return await TagController.get_all_tags(session)


@tag_router.get("/{tag_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=TagRead)
@route_with_action('get_tag_by_id')
async def get_tag_by_id(tag_id: int, session: AsyncSession = Depends(get_session)):
    return await TagController.get_tag_by_id(tag_id, session)


@route_with_action('get_tag_by_name')
@tag_router.get("/{tag_name}/name", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=TagRead)
async def get_tag_by_name(tag_name: str, session: AsyncSession = Depends(get_session)):
    return await TagController.get_tag_by_name(tag_name, session)


@route_with_action('update_tag')
@tag_router.put("/{tag_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=TagRead)
async def update_tag(tag_id: int, tag_data: TagUpdate, session: AsyncSession = Depends(get_session)):
    return await TagController.update_tag(tag_id, tag_data, session)


@route_with_action('delete_tag')
@tag_router.delete("/{tag_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(tag_id: int, session: AsyncSession = Depends(get_session)):
    return await TagController.delete_tag(tag_id, session)
