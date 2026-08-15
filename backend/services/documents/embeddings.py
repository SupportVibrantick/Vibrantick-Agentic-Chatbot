from __future__ import annotations

import asyncio

from sentence_transformers import SentenceTransformer

from core.settings import settings


class EmbeddingService:
    """
    BGE-M3 embedding service.

    Provider:
        BAAI BGE-M3

    Dimension:
        1024
    """

    def __init__(self) -> None:
        self.model = SentenceTransformer(
            settings.EMBEDDING_MODEL,
        )

    async def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        if not texts:
            return []

        embeddings = await asyncio.to_thread(
            self.model.encode,
            texts,
            normalize_embeddings=True,
        )

        return embeddings.tolist()

    async def embed_query(
        self,
        query: str,
    ) -> list[float]:
        embedding = await asyncio.to_thread(
            self.model.encode,
            query,
            normalize_embeddings=True,
        )

        return embedding.tolist()