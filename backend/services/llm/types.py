from __future__ import annotations

from abc import ABC, abstractmethod

from services.llm.types import (
    LLMRequest,
    LLMResponse,
)


class BaseLLMProvider(ABC):
    """
    Abstract base class for all LLM providers.
    """

    @abstractmethod
    async def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        """
        Generate a response from the language model.
        """
        raise NotImplementedError