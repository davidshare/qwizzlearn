from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from src.config import Config

async_engine = create_async_engine(
    Config.DATABASE_URL,
    echo=True
)


async def db_init():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


class AsyncSessionWrapper:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def exec(self, statement):
        result = await self._session.execute(statement)
        return result.scalars()

    def __getattr__(self, name):
        return getattr(self._session, name)


@asynccontextmanager
async def get_session():
    async with AsyncSessionLocal() as session:
        try:
            yield AsyncSessionWrapper(session)
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
