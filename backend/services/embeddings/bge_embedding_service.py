from __future__ import annotations

import asyncio
from sentence_transformers import SentenceTransformer

from core.settings import settings
from services.embeddings.embedding_service import EmbeddingService


class BGEEmbeddingService(EmbeddingService):
    """
    BGE-M3 embedding service implementing EmbeddingService.
    """

    def __init__(self) -> None:
        self.model = SentenceTransformer(
            settings.EMBEDDING_MODEL,
        )

    async def embed_text(
        self,
        text: str,
    ) -> list[float]:
        embedding = await asyncio.to_thread(
            self.model.encode,
            text,
            normalize_embeddings=True,
        )
        return embedding.tolist()

    async def embed_texts(
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
