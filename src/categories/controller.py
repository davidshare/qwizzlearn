from typing import List
from fastapi import Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
import logging

from src.db.main import get_session
from src.authentication.models import User
from .service import CategoryService
from .schemas import CategoryCreate, CategoryRead, CategoryUpdate

logger = logging.getLogger(__name__)

category_service = CategoryService()


class CategoryController:
    @staticmethod
    async def create_category(category_data: List[CategoryCreate], user: User, session: AsyncSession = Depends(get_session)) -> CategoryRead:
        if not user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User ID is missing. You need a valid user to create create a category."
            )

        return await category_service.create_category(category_data, user.id, session)

    @staticmethod
    async def get_category_by_id(category_id: int, session: AsyncSession = Depends(get_session)):
        category = await category_service.get_category_by_id(category_id, session)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        return category

    @staticmethod
    async def get_category_by_name(category_name: str, session: AsyncSession = Depends(get_session)):
        category = await category_service.get_category_by_name(category_name, session)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        return category

    @staticmethod
    async def get_all_categories(session: AsyncSession = Depends(get_session)):
        categories = await category_service.get_all_categories(session)
        if not categories:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No categories available"
            )
        return categories

    @staticmethod
    async def update_category(category_id: int, category_data: CategoryUpdate, session: AsyncSession = Depends(get_session)):
        category = await category_service.update_category(category_id, category_data, session)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        return category

    @staticmethod
    async def delete_category(category_id: int, session: AsyncSession = Depends(get_session)):
        success = await category_service.delete_category(category_id, session)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        return {"message": "Category deleted successfully"}
