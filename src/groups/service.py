from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import func
from sqlmodel import select
from .schemas import (GroupCreate, GroupRead, GroupUpdate)
from .models import Group


class GroupService:
    async def create_group(self, groups_data: GroupCreate, user_id: int, session: AsyncSession) -> GroupRead:
        existing_groups = []
        new_groups = []

        for group in groups_data:
            result = await session.exec(
                select(Group).where(
                    Group.name == group.name)
            )
            existing_category = result.first()

            if existing_category:
                existing_groups.append(existing_category)
            else:
                new_group = Group(
                    **group.model_dump(), created_by=user_id)
                new_groups.append(new_group)

        session.add_all(new_groups)

        await session.commit()

        for group in new_groups:
            await session.refresh(group)

        return existing_groups + new_groups

    async def get_group_by_name(self, name: str, session: AsyncSession) -> GroupRead:
        statement = select(Group).where(
            func.lower(Group.name) == func.lower(name))
        result = await session.exec(statement)
        group = result.first()
        return group

    async def get_group_by_id(self, group_id: int, session: AsyncSession) -> GroupRead:
        statement = select(Group).where(Group.id == group_id)
        result = await session.exec(statement)
        group = result.first()
        return group

    async def get_all_groups(self, session: AsyncSession) -> list[GroupRead]:
        statement = select(Group)
        groups = await session.exec(statement)
        return groups.all()

    async def update_group(self, group_id: int, group_data: GroupUpdate, session: AsyncSession) -> GroupRead:
        statement = select(Group).where(Group.id == group_id)
        result = await session.exec(statement)
        group = result.first()

        if not group:
            return None

        for key, value in group_data.dict(exclude_unset=True).items():
            setattr(group, key, value)

        session.add(group)
        await session.commit()
        session.refresh(group)
        return group

    async def delete_group(self, group_id: int, session: AsyncSession) -> bool:
        statement = select(Group).where(Group.id == group_id)
        result = await session.exec(statement)
        group = result.first()

        if not group:
            return False

        await session.delete(group)
        await session.commit()
        return True
