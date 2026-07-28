from typing import Any, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

T = TypeVar("T", bound=DeclarativeBase)


class BaseSeeder:
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def add(self, instance: T) -> T:
        self.session.add(instance)
        await self.session.flush()
        return instance

    async def flush(self) -> None:
        await self.session.flush()
    async def rollback(self) -> None:
        await self.session.rollback()

    async def refresh(self, instance: T) -> T:
        await self.session.refresh(instance)
        return instance

    async def get_by_id(
        self,
        model: type[T],
        object_id: Any,
        ) -> T | None:
        
            id_column = getattr(model, "id")

            stmt = select(model).where(id_column == object_id)

            result = await self.session.execute(stmt)

            return result.scalar_one_or_none()