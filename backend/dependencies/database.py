
from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import get_db
from database.unit_of_work import UnitOfWork


async def get_uow(
    db: AsyncSession = Depends(get_db),
) -> AsyncGenerator[UnitOfWork, None]:
    """
    Provide a UnitOfWork using the request's database session.

    This keeps repositories and other database dependencies
    inside the same AsyncSession.
    """

    async with UnitOfWork(db) as uow:
        yield uow
