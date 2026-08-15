from __future__ import annotations

from openai import AsyncOpenAI

from core.settings import settings


class EmbeddingService:
    """
    Generates embeddings for document chunks.
    """

    def __init__(self) -> None:
        self.client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY,
        )

    async def embed(
        self,
        text: str,
        model: str = "text-embedding-3-small",
    ) -> list[float]:
        """
        Generate an embedding for a single text.
        """

        response = await self.client.embeddings.create(
            model=model,
            input=text,
        )

        return response.data[0].embedding

    async def embed_many(
        self,
        texts: list[str],
        model: str = "text-embedding-3-small",
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.
        """

        response = await self.client.embeddings.create(
            model=model,
            input=texts,
        )

        return [
            item.embedding
            for item in response.data
        ]