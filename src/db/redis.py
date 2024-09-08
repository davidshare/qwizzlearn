import redis.asyncio as redis
from src.config import Config

JTI_EXPIRY = 3600

# Create a global connection pool
redis_pool = redis.ConnectionPool(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    decode_responses=True
)


async def get_redis_connection():
    return redis.Redis(connection_pool=redis_pool)


async def add_jti_to_blocklist(jti: str) -> None:
    async with await get_redis_connection() as r:
        await r.set(name=jti, value="", ex=JTI_EXPIRY)


async def token_in_blocklist(jti: str) -> bool:
    async with await get_redis_connection() as r:
        value = await r.get(jti)
    return value is not None
