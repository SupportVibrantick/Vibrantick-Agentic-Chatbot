from __future__ import annotations

from collections.abc import AsyncIterator

from openai import AsyncOpenAI

from core.settings import settings

from services.llm.base import BaseLLMService
from services.llm.types import (
    LLMRequest,
)


class DeepSeekService(BaseLLMService):
    """
    DeepSeek implementation of the LLM interface.
    Supports both normal and streaming responses.
    """

    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url=settings.DEEPSEEK_BASE_URL,
        )

    async def chat(
        self,
        request: LLMRequest,
    ) -> str:

        response = await self.client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=[
                {
                    "role": message.role.value,
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
            model=settings.LLM_MODEL,
            messages=[
                {
                    "role": message.role.value,
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

            if (
                delta is not None
                and delta.content is not None
            ):
                yield delta.content