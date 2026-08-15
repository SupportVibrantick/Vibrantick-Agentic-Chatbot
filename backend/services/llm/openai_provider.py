from __future__ import annotations

from collections.abc import AsyncIterator
from openai import AsyncOpenAI

from core.settings import settings
from services.llm.base import BaseLLMService
from services.llm.types import LLMRequest


class OpenAIProvider(BaseLLMService):
    """
    OpenAI implementation of the BaseLLMService interface.
    """

    def __init__(self) -> None:
        self.client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY or "dummy_key",
        )

    async def chat(
        self,
        request: LLMRequest,
    ) -> str:
        response = await self.client.chat.completions.create(
            model=settings.LLM_MODEL or "gpt-4o-mini",
            messages=[
                {
                    "role": message.role.value if hasattr(message.role, "value") else str(message.role),
                    "content": message.content,
                }
                for message in request.messages
            ],
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
        return response.choices[0].message.content or ""

    async def stream(
        self,
        request: LLMRequest,
    ) -> AsyncIterator[str]:
        stream = await self.client.chat.completions.create(
            model=settings.LLM_MODEL or "gpt-4o-mini",
            messages=[
                {
                    "role": message.role.value if hasattr(message.role, "value") else str(message.role),
                    "content": message.content,
                }
                for message in request.messages
            ],
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=True,
        )

        async for chunk in stream:
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta
            if delta is not None and delta.content is not None:
                yield delta.content