from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from models.document_chunk import DocumentChunk
from repositories.document_chunk_repository import (
    DocumentChunkRepository,
)
from services.documents.embeddings import EmbeddingService


class VectorSearchService:
    """
    Semantic search over document chunks using pgvector.
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.repository = DocumentChunkRepository(session)
        self.embedding_service = EmbeddingService()

    async def search(
        self,
        *,
        query: str,
        knowledge_base_id: int,
        top_k: int = 5,
    ) -> list[DocumentChunk]:
        query_embedding = (
            await self.embedding_service.embed_query(
                query,
            )
        )

        return await self.repository.similarity_search(
            knowledge_base_id=knowledge_base_id,
            embedding=query_embedding,
            limit=top_k,
        )