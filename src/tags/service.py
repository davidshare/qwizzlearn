from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import func
from sqlmodel import select
from .schemas import TagCreate, TagRead, TagUpdate
from .models.tags import Tag


class TagService:
    async def create_tag(self, tags_data: TagCreate, user_id: int, session: AsyncSession) -> list[TagRead]:
        existing_tags = []
        new_tags = []

        for tag in tags_data:
            result = await session.exec(
                select(Tag).where(
                    Tag.name == tag.name)
            )
            existing_tag = result.first()

            if existing_tag:
                existing_tags.append(existing_tag)
            else:
                new_tag = Tag(
                    **tag.model_dump(), created_by=user_id)
                new_tags.append(new_tag)

        session.add_all(new_tags)

        await session.commit()

        for tag in new_tags:
            await session.refresh(tag)

        return existing_tags + new_tags

    async def get_tag_by_name(self, name: str, session: AsyncSession) -> TagRead:
        statement = select(Tag).where(
            func.lower(Tag.name) == func.lower(name)
        )
        result = await session.exec(statement)
        tag = result.first()
        return tag

    async def get_tag_by_id(self, tag_id: int, session: AsyncSession) -> TagRead:
        statement = select(Tag).where(Tag.id == tag_id)
        result = await session.exec(statement)
        tag = result.first()
        return tag

    async def get_all_tags(self, session: AsyncSession) -> list[TagRead]:
        statement = select(Tag)
        tags = await session.exec(statement)
        return tags.all()

    async def update_tag(self, tag_id: int, tag_data: TagUpdate, session: AsyncSession) -> TagRead:
        statement = select(Tag).where(Tag.id == tag_id)
        result = await session.exec(statement)
        tag = result.first()

        if not tag:
            return None

        for key, value in tag_data.dict(exclude_unset=True).items():
            setattr(tag, key, value)

        session.add(tag)
        await session.commit()
        session.refresh(tag)
        return tag

    async def delete_tag(self, tag_id: int, session: AsyncSession) -> bool:
        statement = select(Tag).where(Tag.id == tag_id)
        result = await session.exec(statement)
        tag = result.first()

        if not tag:
            return False

        await session.delete(tag)
        await session.commit()
        return True
