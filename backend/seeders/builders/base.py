from __future__ import annotations

from abc import ABC
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession


class BuilderBase(ABC):
    """
    Base class for all entity builders.

    Builders are responsible only for creating and retrieving
    entities. They never commit transactions.

    Transaction management is handled by the ExecutionManager.
    """

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, instance: Any) -> None:
        """
        Add an entity to the current session.
        """
        self.session.add(instance)

    async def flush(self) -> None:
        """
        Flush pending changes.
        """
        await self.session.flush()

    async def refresh(self, instance: Any) -> None:
        """
        Refresh an entity from the database.
        """
        await self.session.refresh(instance)

    async def persist(self, instance: Any) -> None:
        """
        Add, flush and refresh an entity.
        """
        await self.add(instance)
        await self.flush()
        await self.refresh(instance)