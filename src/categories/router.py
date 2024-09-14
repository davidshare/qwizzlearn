from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.authentication.dependencies import AccessTokenBearer, get_current_user
from src.authorisation.dependencies import route_with_action, authorize
from src.db.main import get_session

from .controller import CategoryController
from .schemas import CategoryCreate, CategoryRead, CategoryUpdate

category_router = APIRouter()
access_token_bearer = AccessTokenBearer()


@route_with_action('create_category')
@category_router.post("/", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_201_CREATED, response_model=List[CategoryRead])
async def create_category(category_data: List[CategoryCreate], user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await CategoryController.create_category(category_data, user, session)


@category_router.get("/", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=List[CategoryRead])
@route_with_action('get_all_categories')
async def get_all_categories(session: AsyncSession = Depends(get_session)):
    return await CategoryController.get_all_categories(session)


@category_router.get("/{category_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=CategoryRead)
@route_with_action('get_category_by_id')
async def get_category_by_id(category_id: int, session: AsyncSession = Depends(get_session)):
    return await CategoryController.get_category_by_id(category_id, session)


@route_with_action('get_category_by_name')
@category_router.get("/{category_name}/name", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=CategoryRead)
async def get_category_by_name(category_name: str, session: AsyncSession = Depends(get_session)):
    return await CategoryController.get_category_by_name(category_name, session)


@route_with_action('update_category')
@category_router.put("/{category_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK, response_model=CategoryRead)
async def update_category(category_id: int, category_data: CategoryUpdate, session: AsyncSession = Depends(get_session)):
    return await CategoryController.update_category(category_id, category_data, session)


@route_with_action('delete_category')
@category_router.delete("/{category_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int, session: AsyncSession = Depends(get_session)):
    return await CategoryController.delete_category(category_id, session)
