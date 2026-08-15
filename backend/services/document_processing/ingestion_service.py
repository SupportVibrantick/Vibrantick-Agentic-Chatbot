from __future__ import annotations

from datetime import UTC, datetime

from database.unit_of_work import UnitOfWork
from models.document_chunk import DocumentChunk
from models.knowledge_source import (
    KnowledgeSource,
    KnowledgeSourceStatus,
)

from services.document_processing.chunker import (
    DocumentChunker,
)
from services.document_processing.embedding_service import (
    EmbeddingService,
)
from services.document_processing.extractor import (
    DocumentExtractor,
)


class IngestionService:
    """
    Complete document ingestion pipeline.

    Upload
        ↓
    Extract
        ↓
    Chunk
        ↓
    Embed
        ↓
    Store
    """

    def __init__(self) -> None:

        self.extractor = DocumentExtractor()
        self.chunker = DocumentChunker()
        self.embedding_service = EmbeddingService()

    async def ingest(
        self,
        knowledge_source: KnowledgeSource,
        uow: UnitOfWork,
    ) -> None:

        knowledge_source.status = (
            KnowledgeSourceStatus.PROCESSING
        )

        await uow.flush()

        try:

            knowledge_base = (
                knowledge_source.knowledge_base
            )

            text = await self.extractor.extract(
                file_path=knowledge_source.file_path,
                source_type=knowledge_source.source_type,
            )

            chunks = self.chunker.chunk(
                text=text,
                chunk_size=knowledge_base.chunk_size,
                chunk_overlap=knowledge_base.chunk_overlap,
            )

            embeddings = (
                await self.embedding_service.embed_many(
                    chunks,
                    model=knowledge_base.embedding_model,
                )
            )

            for index, (chunk, embedding) in enumerate(
                zip(chunks, embeddings)
            ):

                document_chunk = DocumentChunk(
                    document_id=knowledge_source.id,
                    chunk_index=index,
                    content=chunk,
                    token_count=len(
                        self.chunker.encoding.encode(chunk)
                    ),
                    embedding=embedding,
                )

                await uow.document_chunks.add(
                    document_chunk,
                )

            knowledge_source.status = (
                KnowledgeSourceStatus.READY
            )

            knowledge_source.processed_at = (
                datetime.now(UTC)
            )

            await uow.commit()

        except Exception:

            knowledge_source.status = (
                KnowledgeSourceStatus.FAILED
            )

            await uow.commit()

            raise