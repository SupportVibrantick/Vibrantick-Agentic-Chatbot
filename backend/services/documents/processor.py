from __future__ import annotations

from database.unit_of_work import UnitOfWork

from models.document import (
    Document,
    DocumentStatus,
)

from models.document_chunk import DocumentChunk

from services.documents.chunker import (
    DocumentChunker,
)

from services.documents.embeddings import (
    EmbeddingService,
)

from services.documents.extractor import (
    DocumentExtractor,
)


class DocumentProcessor:
    """
    Canonical document ingestion pipeline.

    PDF
      ↓
    Extract text
      ↓
    Chunk text
      ↓
    Generate BGE-M3 embeddings
      ↓
    Store document chunks
      ↓
    READY
    """

    def __init__(self) -> None:
        self.extractor = DocumentExtractor()
        self.chunker = DocumentChunker()
        self.embedding_service = EmbeddingService()

    async def process(
        self,
        document: Document,
        uow: UnitOfWork,
    ) -> None:

        document.status = DocumentStatus.PROCESSING

        await uow.flush()

        try:
            # ---------------------------------------------
            # Extract
            # ---------------------------------------------

            text = await self.extractor.extract_text(
                document.storage_path,
            )

            # ---------------------------------------------
            # Chunk
            # ---------------------------------------------

            chunks = await self.chunker.chunk_text(
                text,
            )

            if not chunks:
                raise ValueError(
                    "No usable text was extracted from the document."
                )

            # ---------------------------------------------
            # Embeddings
            # ---------------------------------------------

            embeddings = (
                await self.embedding_service.embed_documents(
                    chunks,
                )
            )

            if len(chunks) != len(embeddings):
                raise RuntimeError(
                    "Embedding count does not match chunk count."
                )

            # ---------------------------------------------
            # Store chunks
            # ---------------------------------------------

            document_chunks: list[DocumentChunk] = []

            for index, (chunk, embedding) in enumerate(
                zip(chunks, embeddings)
            ):
                document_chunks.append(
                    DocumentChunk(
                        document_id=document.id,
                        chunk_index=index,
                        content=chunk,
                        token_count=len(chunk.split()),
                        embedding=embedding,
                    )
                )

            await uow.document_chunks.create_many(
                document_chunks,
            )

            # ---------------------------------------------
            # Complete
            # ---------------------------------------------

            document.status = DocumentStatus.READY

            await uow.commit()

        except Exception:
            document.status = DocumentStatus.FAILED

            await uow.commit()

            raise