from __future__ import annotations

from services.llm.base import BaseLLMProvider
from services.llm.openai_provider import OpenAIProvider
from models.chatbot_ai_config import LLMProvider


class ProviderFactory:
    """
    Creates the appropriate LLM provider.
    """

    @staticmethod
    def create(
        provider: LLMProvider,
    ) -> BaseLLMProvider:
        if provider == LLMProvider.OPENAI:
            return OpenAIProvider()

        raise ValueError(
            f"Unsupported LLM provider: {provider}"
        )