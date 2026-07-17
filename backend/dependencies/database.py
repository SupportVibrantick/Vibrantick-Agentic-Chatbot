from collections.abc import AsyncGenerator

from database.unit_of_work import UnitOfWork


async def get_uow() -> AsyncGenerator[UnitOfWork, None]:
    """
    FastAPI dependency that provides a UnitOfWork.

    A new UnitOfWork (and therefore a new database session)
    is created for each request.
    """

    async with UnitOfWork() as uow:
        yield uow