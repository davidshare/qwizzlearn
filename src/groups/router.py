from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.authentication.dependencies import AccessTokenBearer, get_current_user
from src.authorisation.dependencies import route_with_action, authorize
from src.db.main import get_session

from .controller import GroupController
from .schemas import GroupCreate, GroupRead, GroupUpdate

group_router = APIRouter()
access_token_bearer = AccessTokenBearer()


@route_with_action('create_group')
@group_router.post("/", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_201_CREATED, response_model=List[GroupRead])
async def create_group(group_data: List[GroupCreate], user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await GroupController.create_group(group_data, user, session)


@group_router.get("/", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=List[GroupRead])
@route_with_action('get_all_groups')
async def get_all_groups(session: AsyncSession = Depends(get_session)):
    return await GroupController.get_all_groups(session)


@group_router.get("/{group_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=GroupRead)
@route_with_action('get_group_by_id')
async def get_group_by_id(group_id: int, session: AsyncSession = Depends(get_session)):
    return await GroupController.get_group_by_id(group_id, session)


@route_with_action('get_group_by_name')
@group_router.get("/{group_name}/name", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=GroupRead)
async def get_group_by_name(group_name: str, session: AsyncSession = Depends(get_session)):
    return await GroupController.get_group_by_name(group_name, session)


@route_with_action('update_group')
@group_router.put("/{group_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=GroupRead)
async def update_group(group_id: int, group_data: GroupUpdate, session: AsyncSession = Depends(get_session)):
    return await GroupController.update_group(group_id, group_data, session)


@route_with_action('delete_group')
@group_router.delete("/{group_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_204_NO_CONTENT)
async def delete_group(group_id: int, session: AsyncSession = Depends(get_session)):
    return await GroupController.delete_group(group_id, session)
