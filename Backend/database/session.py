from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as db:
        yield db