from typing import List
from fastapi import Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
import logging

from src.db.main import get_session
from src.authentication.models import User
from .service import TagService
from .schemas import TagCreate, TagRead, TagUpdate

logger = logging.getLogger(__name__)

tag_service = TagService()


class TagController:
    @staticmethod
    async def create_tag(tag_data: List[TagCreate], user: User, session: AsyncSession = Depends(get_session)) -> List[TagRead]:
        if not user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User ID is missing. You need a valid user to create a tag."
            )

        return await tag_service.create_tag(tag_data, user.id, session)

    @staticmethod
    async def get_tag_by_id(tag_id: int, session: AsyncSession = Depends(get_session)):
        tag = await tag_service.get_tag_by_id(tag_id, session)
        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag not found"
            )
        return tag

    @staticmethod
    async def get_tag_by_name(tag_name: str, session: AsyncSession = Depends(get_session)):
        tag = await tag_service.get_tag_by_name(tag_name, session)
        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag not found"
            )
        return tag

    @staticmethod
    async def get_all_tags(session: AsyncSession = Depends(get_session)):
        tags = await tag_service.get_all_tags(session)
        if not tags:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No tags available"
            )
        return tags

    @staticmethod
    async def update_tag(tag_id: int, tag_data: TagUpdate, session: AsyncSession = Depends(get_session)):
        tag = await tag_service.update_tag(tag_id, tag_data, session)
        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag not found"
            )
        return tag

    @staticmethod
    async def delete_tag(tag_id: int, session: AsyncSession = Depends(get_session)):
        success = await tag_service.delete_tag(tag_id, session)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag not found"
            )
        return {"message": "Tag deleted successfully"}
