from collections.abc import AsyncGenerator

from database.unit_of_work import UnitOfWork


async def get_uow() -> AsyncGenerator[UnitOfWork, None]:
    """
    Provide a UnitOfWork that owns its database session
    and transaction for the duration of the request.
    """
    async with UnitOfWork() as uow:
        yield uow