from __future__ import annotations

from abc import ABC
from typing import Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class Factory(ABC, Generic[T]):
    """
    Base factory for building and persisting test objects.

    Child factories only need to implement `build()`.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def build(self, **kwargs) -> T:
        """
        Build an object without saving it.
        """
        raise NotImplementedError

    async def create(self, **kwargs) -> T:
        """
        Build and persist an object.
        """
        obj = await self.build(**kwargs)

        self.session.add(obj)

        await self.session.flush()
        await self.session.refresh(obj)

        return obj

    async def create_batch(
        self,
        count: int,
        **kwargs,
    ) -> list[T]:
        """
        Create multiple persisted objects.
        """
        objects = []

        for _ in range(count):
            obj = await self.build(**kwargs)
            self.session.add(obj)
            objects.append(obj)
            await self.session.flush()

        for obj in objects:
            await self.session.refresh(obj)

        return objects