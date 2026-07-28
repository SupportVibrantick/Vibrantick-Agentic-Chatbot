from __future__ import annotations

from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from tools.core.context import ExecutionContext


class BaseSeed(ABC):
    """
    Base class for all executable seed tasks.

    Responsibilities:
    - Provide access to the shared execution context.
    - Provide access to the shared database session.
    - Define the run() contract.
    """

    

    def __init__(self, context: ExecutionContext) -> None:
        self.context = context
        self.session: AsyncSession = context.db

    @abstractmethod
    async def run(self) -> None:
        """
        Execute the seed task.
        """
        raise NotImplementedError