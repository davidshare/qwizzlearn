from typing import List
from fastapi import Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
import logging

from src.db.main import get_session
from src.authentication.models import User
from .service import GroupService
from .schemas import GroupCreate, GroupRead, GroupUpdate

logger = logging.getLogger(__name__)

group_service = GroupService()


class GroupController:
    @staticmethod
    async def create_group(group_data: List[GroupCreate], user: User, session: AsyncSession = Depends(get_session)) -> GroupRead:
        if not user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User ID is missing. You need a valid user to create a group."
            )

        return await group_service.create_group(group_data, user.id, session)

    @staticmethod
    async def get_group_by_id(group_id: int, session: AsyncSession = Depends(get_session)):
        group = await group_service.get_group_by_id(group_id, session)
        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group not found"
            )
        return group

    @staticmethod
    async def get_group_by_name(group_name: str, session: AsyncSession = Depends(get_session)):
        group = await group_service.get_group_by_name(group_name, session)
        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group not found"
            )
        return group

    @staticmethod
    async def get_all_groups(session: AsyncSession = Depends(get_session)):
        groups = await group_service.get_all_groups(session)
        if not groups:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No groups available"
            )
        return groups

    @staticmethod
    async def update_group(group_id: int, group_data: GroupUpdate, session: AsyncSession = Depends(get_session)):
        group = await group_service.update_group(group_id, group_data, session)
        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group not found"
            )
        return group

    @staticmethod
    async def delete_group(group_id: int, session: AsyncSession = Depends(get_session)):
        success = await group_service.delete_group(group_id, session)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group not found"
            )
        return {"message": "Group deleted successfully"}
