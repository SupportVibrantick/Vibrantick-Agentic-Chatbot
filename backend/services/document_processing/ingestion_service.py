from __future__ import annotations

from datetime import UTC, datetime

from database.unit_of_work import UnitOfWork
from models.document import Document, DocumentStatus
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

    Document
        ↓
    Extract
        ↓
    Chunk
        ↓
    Embed
        ↓
    Store DocumentChunks
    """

    def __init__(self) -> None:
        self.extractor = DocumentExtractor()
        self.chunker = DocumentChunker()
        self.embedding_service = EmbeddingService()

    async def ingest(
        self,
        document: Document,
        knowledge_source: KnowledgeSource,
        uow: UnitOfWork,
    ) -> None:
        """
        Process a Document and store its vectorized chunks.

        KnowledgeSource represents the origin/source metadata.
        Document represents the actual ingested document.
        DocumentChunk references Document.id.
        """

        knowledge_source.status = (
            KnowledgeSourceStatus.PROCESSING
        )

        document.status = DocumentStatus.PROCESSING

        await uow.flush()

        try:
            # -----------------------------------------------------
            # Get Knowledge Base
            # -----------------------------------------------------
            knowledge_base = (
                await uow.knowledge_bases.get_by_id(
                    document.knowledge_base_id
                )
            )

            if knowledge_base is None:
                raise ValueError(
                    "Knowledge base not found."
                )

            # -----------------------------------------------------
            # Extract text
            # -----------------------------------------------------
            text = await self.extractor.extract(
                file_path=knowledge_source.file_path,
                source_type=knowledge_source.source_type,
            )

            # -----------------------------------------------------
            # Chunk text
            # -----------------------------------------------------
            chunks = self.chunker.chunk(
                text=text,
                chunk_size=knowledge_base.chunk_size,
                chunk_overlap=knowledge_base.chunk_overlap,
            )

            # -----------------------------------------------------
            # Generate embeddings
            # -----------------------------------------------------
            embeddings = (
                await self.embedding_service.embed_many(
                    chunks,
                    model=knowledge_base.embedding_model,
                )
            )

            # -----------------------------------------------------
            # Store chunks
            # -----------------------------------------------------
            for index, (chunk, embedding) in enumerate(
                zip(chunks, embeddings)
            ):
                document_chunk = DocumentChunk(
                    document_id=document.id,
                    chunk_index=index,
                    content=chunk,
                    token_count=len(
                        self.chunker.encoding.encode(chunk)
                    ),
                    embedding=embedding,
                )

                await uow.document_chunks.add(
                    document_chunk
                )

            # -----------------------------------------------------
            # Mark successful
            # -----------------------------------------------------
            document.status = DocumentStatus.READY

            knowledge_source.status = (
                KnowledgeSourceStatus.READY
            )

            knowledge_source.processed_at = (
                datetime.now(UTC)
            )

            knowledge_source.error_message = None

            await uow.commit()

        except Exception as exc:
            # -----------------------------------------------------
            # Mark failed
            # -----------------------------------------------------
            document.status = DocumentStatus.FAILED

            knowledge_source.status = (
                KnowledgeSourceStatus.FAILED
            )

            knowledge_source.error_message = str(exc)

            await uow.commit()

            raise