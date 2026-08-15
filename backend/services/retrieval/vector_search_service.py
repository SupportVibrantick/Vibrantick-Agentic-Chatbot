from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.document_chunk import DocumentChunk
from services.document_processing.embedding_service import (
    EmbeddingService,
)


class VectorSearchService:
    """
    Semantic search over document chunks using pgvector.
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session
        self.embedding_service = EmbeddingService()

    async def search(
        self,
        *,
        query: str,
        knowledge_base_id: int,
        embedding_model: str,
        top_k: int = 5,
    ) -> list[DocumentChunk]:

        query_embedding = (
            await self.embedding_service.embed(
                query,
                model=embedding_model,
            )
        )

        stmt = (
            select(DocumentChunk)
            .join(DocumentChunk.knowledge_source)
            .where(
                DocumentChunk.knowledge_source.has(
                    knowledge_base_id=knowledge_base_id
                )
            )
            .order_by(
                DocumentChunk.embedding.cosine_distance(
                    query_embedding
                )
            )
            .limit(top_k)
        )

        result = await self.session.execute(stmt)

        return list(result.scalars().all())