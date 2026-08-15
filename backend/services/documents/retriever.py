from __future__ import annotations

from database.unit_of_work import UnitOfWork

from services.documents.embeddings import EmbeddingService


class DocumentRetriever:
    def __init__(
        self,
        uow: UnitOfWork,
    ):
        self.uow = uow
        self.embedding_service = EmbeddingService()

    async def retrieve(
        self,
        knowledge_base_id: int,
        question: str,
        limit: int = 5,
    ) -> str:

        query_embedding = (
            await self.embedding_service.embed_query(
                question,
            )
        )

        chunks = (
            await self.uow.document_chunks.similarity_search(
                knowledge_base_id=knowledge_base_id,
                embedding=query_embedding,
                limit=limit,
            )
        )

        if not chunks:
            return ""

        return "\n\n".join(
            chunk.content
            for chunk in chunks
        )

    async def retrieve_context(
        self,
        question: str,
        knowledge_base_id: int = 1,
        limit: int = 5,
    ) -> str:
        return await self.retrieve(
            knowledge_base_id=knowledge_base_id,
            question=question,
            limit=limit,
        )