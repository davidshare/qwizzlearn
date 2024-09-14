from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import func
from sqlmodel import select
from .schemas import CategoryCreate, CategoryRead, CategoryUpdate
from .models import Category


class CategoryService:
    async def create_category(self, categories_data: CategoryCreate, user_id: int, session: AsyncSession) -> CategoryRead:
        existing_categories = []
        new_categories = []

        for category in categories_data:
            result = await session.exec(
                select(Category).where(
                    Category.name == category.name)
            )
            existing_category = result.first()

            if existing_category:
                existing_categories.append(existing_category)
            else:
                new_category = Category(
                    **category.model_dump(), created_by=user_id)
                new_categories.append(new_category)

        session.add_all(new_categories)

        await session.commit()

        for category in new_categories:
            await session.refresh(category)

        return existing_categories + new_categories

    async def get_category_by_name(self, name: str, session: AsyncSession) -> CategoryRead:
        statement = select(Category).where(
            func.lower(Category.name) == func.lower(name)
        )
        result = await session.exec(statement)
        category = result.first()
        return category

    async def get_category_by_id(self, category_id: int, session: AsyncSession) -> CategoryRead:
        statement = select(Category).where(Category.id == category_id)
        result = await session.exec(statement)
        category = result.first()
        return category

    async def get_all_categories(self, session: AsyncSession) -> list[CategoryRead]:
        statement = select(Category)
        categories = await session.exec(statement)
        return categories.all()

    async def update_category(self, category_id: int, category_data: CategoryUpdate, session: AsyncSession) -> CategoryRead:
        statement = select(Category).where(Category.id == category_id)
        result = await session.exec(statement)
        category = result.first()

        if not category:
            return None

        for key, value in category_data.dict(exclude_unset=True).items():
            setattr(category, key, value)

        session.add(category)
        await session.commit()
        session.refresh(category)
        return category

    async def delete_category(self, category_id: int, session: AsyncSession) -> bool:
        statement = select(Category).where(Category.id == category_id)
        result = await session.exec(statement)
        category = result.first()

        if not category:
            return False

        await session.delete(category)
        await session.commit()
        return True
