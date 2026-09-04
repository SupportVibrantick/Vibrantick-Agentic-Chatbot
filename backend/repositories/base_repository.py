from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Generic repository providing reusable persistence and query operations.

    Repositories should contain only domain-specific queries.
    Transaction management is handled by the Unit of Work.
    """

    model: type[ModelType]

    def __init__(self, session: AsyncSession):
        self.session = session

    # ==========================================================
    # Persistence
    # ==========================================================

    async def add(
        self,
        instance: ModelType,
    ) -> None:
        """
        Add an entity to the current session.

        Does NOT commit.
        """
        self.session.add(instance)
        
    async def create(
        self,
        instance: ModelType,
        ) -> None:
        """
        Create a new entity in the current session.
        Does NOT commit.
        """
        await self.add(instance)

    async def add_all(
        self,
        instances: Sequence[ModelType],
    ) -> None:
        """
        Add multiple entities to the current session.

        Does NOT commit.
        """
        self.session.add_all(list(instances))

    async def delete(
        self,
        instance: ModelType,
    ) -> None:
        """
        Mark an entity for deletion.

        Does NOT commit.
        """
        await self.session.delete(instance)

    async def flush(self) -> None:
        """
        Flush pending SQL statements.

        Useful for obtaining generated primary keys
        before committing.
        """
        await self.session.flush()

    async def refresh(
        self,
        instance: ModelType,
    ) -> None:
        """
        Refresh an entity from the database.
        """
        await self.session.refresh(instance)

    # ==========================================================
    # Queries
    # ==========================================================

    async def get_by_id(
        self,
        object_id: int,
    ) -> ModelType | None:
        """
        Retrieve an entity by its primary key.
        """
        stmt = (
            select(self.model)
            .filter_by(id=object_id)
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def list(
        self,
    ) -> Sequence[ModelType]:
        """
        Return all entities.
        """
        stmt = select(self.model)

        result = await self.session.execute(stmt)

        return result.scalars().all()

    async def exists(
        self,
        **filters: Any,
    ) -> bool:
        """
        Check whether an entity exists.
        """
        stmt = (
            select(self.model)
            .filter_by(**filters)
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none() is not None