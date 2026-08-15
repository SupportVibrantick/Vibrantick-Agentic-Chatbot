from __future__ import annotations

from sqlalchemy import (
    delete,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession

from models.document import Document, DocumentStatus
from models.document_chunk import DocumentChunk

from repositories.base_repository import BaseRepository

DEFAULT_SEARCH_LIMIT = 5


class DocumentChunkRepository(
    BaseRepository[DocumentChunk],
):
    model = DocumentChunk

    def __init__(
        self,
        session: AsyncSession,
    ):
        super().__init__(session)

    async def list_by_document(
        self,
        document_id: int,
    ) -> list[DocumentChunk]:

        stmt = (
            select(DocumentChunk)
            .where(
                DocumentChunk.document_id == document_id,
            )
            .order_by(
                DocumentChunk.chunk_index,
            )
        )

        result = await self.session.execute(stmt)

        return list(result.scalars().all())

    async def get_by_chunk_index(
        self,
        document_id: int,
        chunk_index: int,
    ) -> DocumentChunk | None:

        stmt = (
            select(DocumentChunk)
            .where(
                DocumentChunk.document_id == document_id,
                DocumentChunk.chunk_index == chunk_index,
            )
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def create_many(
        self,
        chunks: list[DocumentChunk],
    ) -> list[DocumentChunk]:

        self.session.add_all(chunks)

        await self.session.flush()

        return chunks

    async def delete_by_document(
        self,
        document_id: int,
    ) -> None:

        stmt = (
            delete(DocumentChunk)
            .where(
                DocumentChunk.document_id == document_id,
            )
        )

        await self.session.execute(stmt)

        await self.session.flush()

    async def similarity_search(
        self,
        knowledge_base_id: int,
        embedding: list[float],
        limit: int = DEFAULT_SEARCH_LIMIT,
    ) -> list[DocumentChunk]:

        stmt = (
            select(DocumentChunk)
            .join(
                Document,
                Document.id == DocumentChunk.document_id,
            )
            .where(
                Document.knowledge_base_id == knowledge_base_id,
                Document.status == DocumentStatus.READY,
                DocumentChunk.embedding.is_not(None),
            )
            .order_by(
                DocumentChunk.embedding.cosine_distance(
                    embedding,
                )
            )
            .limit(limit)
        )

        result = await self.session.execute(stmt)

        return list(result.scalars().all())