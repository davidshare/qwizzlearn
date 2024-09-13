from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .schemas import DifficultyCreate, DifficultyRead, DifficultyUpdate
from .models import Difficulty


class DifficultyService:
    async def create_difficulty(self, difficulty_data: DifficultyCreate, session: AsyncSession) -> DifficultyRead:
        difficulty_dict = difficulty_data.model_dump()

        new_difficulty = Difficulty(**difficulty_dict)
        session.add(new_difficulty)
        await session.commit()
        session.refresh(new_difficulty)
        return new_difficulty

    async def get_difficulty_by_name(self, name: str, session: AsyncSession) -> DifficultyRead:
        statement = select(Difficulty).where(Difficulty.name == name)
        result = await session.exec(statement)
        difficulty = result.first()
        return difficulty

    async def get_difficulty_by_id(self, difficulty_id: int, session: AsyncSession) -> DifficultyRead:
        statement = select(Difficulty).where(Difficulty.id == difficulty_id)
        result = await session.exec(statement)
        difficulty = result.first()
        return difficulty

    async def get_all_difficulties(self, session: AsyncSession) -> DifficultyRead:
        statement = select(Difficulty)
        difficulties = await session.exec(statement)
        return difficulties

    async def update_difficulty(self, difficulty_id: int, difficulty_data: DifficultyUpdate, session: AsyncSession) -> DifficultyRead:
        statement = select(Difficulty).where(Difficulty.id == difficulty_id)
        result = await session.exec(statement)
        difficulty = result.first()

        if not difficulty:
            return None

        for key, value in difficulty_data.dict(exclude_unset=True).items():
            setattr(difficulty, key, value)

        session.add(difficulty)
        await session.commit()
        session.refresh(difficulty)
        return difficulty

    async def delete_difficulty(self, difficulty_id: int, session: AsyncSession) -> bool:
        statement = select(Difficulty).where(Difficulty.id == difficulty_id)
        result = await session.exec(statement)
        difficulty = result.first()

        if not difficulty:
            return False

        await session.delete(difficulty)
        await session.commit()
        return True
