from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.document import Document, DocumentStatus
from repositories.base_repository import BaseRepository


class DocumentRepository(BaseRepository[Document]):
    model = Document

    def __init__(
        self,
        session: AsyncSession,
    ):
        super().__init__(session)

    async def list_by_knowledge_base(
        self,
        knowledge_base_id: int,
    ) -> list[Document]:
        stmt = (
            select(Document)
            .where(
                Document.knowledge_base_id == knowledge_base_id,
            )
            .order_by(Document.created_at.desc())
        )

        result = await self.session.execute(stmt)

        return list(result.scalars().all())

    async def get_by_filename(
        self,
        knowledge_base_id: int,
        original_filename: str,
    ) -> Document | None:
        stmt = (
            select(Document)
            .where(
                Document.knowledge_base_id == knowledge_base_id,
                Document.original_filename == original_filename,
            )
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def exists_by_filename(
        self,
        knowledge_base_id: int,
        original_filename: str,
    ) -> bool:
        return (
            await self.get_by_filename(
                knowledge_base_id,
                original_filename,
            )
            is not None
        )

    async def list_by_status(
        self,
        knowledge_base_id: int,
        status: DocumentStatus,
    ) -> list[Document]:
        stmt = (
            select(Document)
            .where(
                Document.knowledge_base_id == knowledge_base_id,
                Document.status == status,
            )
            .order_by(Document.created_at.desc())
        )

        result = await self.session.execute(stmt)

        return list(result.scalars().all())

    async def update_status(
        self,
        document: Document,
        status: DocumentStatus,
    ) -> Document:
        document.status = status

        await self.session.flush()
        await self.session.refresh(document)

        return document

    async def get_processing_documents(
        self,
    ) -> list[Document]:
        stmt = (
            select(Document)
            .where(
                Document.status == DocumentStatus.PROCESSING,
            )
            .order_by(Document.created_at)
        )

        result = await self.session.execute(stmt)

        return list(result.scalars().all())