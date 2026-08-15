from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from services.llm.types import LLMRequest


class BaseLLMService(ABC):
    """
    Base interface implemented by every LLM provider.
    """

    @abstractmethod
    async def chat(
        self,
        request: LLMRequest,
    ) -> str:
        """
        Generate a complete response.
        """
        raise NotImplementedError

    @abstractmethod
    async def stream(
        self,
        request: LLMRequest,
    ) -> AsyncIterator[str]:
        """
        Stream the response token-by-token.
        """
        raise NotImplementedError