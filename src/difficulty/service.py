from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .schemas import DifficultyCreate, DifficultyRead
from .models import Difficulty


class DifficultyService:
    async def get_difficulty_by_name(self, name: str, session: AsyncSession) -> DifficultyRead:
        statement = select(Difficulty).where(Difficulty.name == name)
        result = await session.exec(statement)
        difficulty = result.first()
        return difficulty

    async def difficulty_exists(self, name: str, session: AsyncSession):
        if not name:
            raise ValueError("The difficulty name must be provided")
        difficulty = await self.get_difficulty_by_name(name, session)
        return difficulty

    async def create_difficulty(self, difficulty_data: DifficultyCreate, session: AsyncSession) -> DifficultyRead:
        difficulty_dict = difficulty_data.model_dump()

        new_difficulty = Difficulty(**difficulty_dict)
        session.add(new_difficulty)
        await session.commit()
        session.refresh(new_difficulty)
        return new_difficulty
