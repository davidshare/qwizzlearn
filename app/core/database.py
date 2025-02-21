from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import config

async_engine = AsyncEngine(
    create_engine(url=config.DB_URL, echo=config.ENV == "development", future=True)
)

async_session_factory = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def db_init():
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        print("Database initialized successfully")
    except Exception as e:
        print(f"Failed to initialize database: {str(e)}")
        raise


async def get_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session
