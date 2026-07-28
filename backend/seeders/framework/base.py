from __future__ import annotations

from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from seeders.framework.context import ExecutionContext


class BaseSeeder(ABC):
    """
    Base class for all seeders.
    """

    name: str = ""
    priority: int = 100
    depends_on: tuple[type["BaseSeeder"], ...] = ()

    def __init__(
        self,
        context: ExecutionContext,
    ) -> None:
        self.context = context
        self.session: AsyncSession = context.db

    async def before_run(self) -> None:
        """
        Hook executed before the seeder runs.

        Override in subclasses if pre-processing is required.
        """
        pass

    @abstractmethod
    async def run(self) -> None:
        """
        Execute the seeder.
        """
        raise NotImplementedError

    async def after_run(self) -> None:
        """
        Hook executed after the seeder runs.

        Override in subclasses if post-processing is required.
        """
        pass