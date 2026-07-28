from __future__ import annotations

from openai import AsyncOpenAI

from core.settings import settings
from services.llm.base import BaseLLMProvider
from services.llm.types import (
    LLMMessage,
    LLMRequest,
    LLMResponse,
)


class OpenAIProvider(BaseLLMProvider):
    """
    OpenAI implementation of the BaseLLMProvider.
    """

    def __init__(self) -> None:
        self._client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY,
        )

    async def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        messages = [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in request.messages
        ]

        response = await self._client.chat.completions.create(
            model=request.model,
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

        choice = response.choices[0]

        return LLMResponse(
            content=choice.message.content or "",
            model=response.model,
            finish_reason=choice.finish_reason,
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
            total_tokens=response.usage.total_tokens,
        )