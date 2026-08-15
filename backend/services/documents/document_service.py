from __future__ import annotations

import shutil
import uuid
from pathlib import Path

from fastapi import UploadFile

from database.unit_of_work import UnitOfWork

from models.document import (
    Document,
    DocumentStatus,
)

from services.documents.processor import (
    DocumentProcessor,
)

UPLOAD_DIRECTORY = Path("uploads/documents")


class DocumentService:
    def __init__(
        self,
        uow: UnitOfWork,
    ):
        self.uow = uow

        self.processor = DocumentProcessor()

        UPLOAD_DIRECTORY.mkdir(
            parents=True,
            exist_ok=True,
        )

    async def upload_document(
        self,
        knowledge_base_id: int,
        file: UploadFile,
    ) -> Document:

        knowledge_base = (
            await self.uow.knowledge_bases.get_by_id(
                knowledge_base_id,
            )
        )

        if knowledge_base is None:
            raise ValueError(
                "Knowledge Base not found."
            )

        if not file.filename:
            raise ValueError(
                "Filename is required."
            )

        extension = Path(
            file.filename,
        ).suffix.lower()

        if extension != ".pdf":
            raise ValueError(
                "Only PDF files are supported."
            )

        exists = (
            await self.uow.documents.exists_by_filename(
                knowledge_base_id,
                file.filename,
            )
        )

        if exists:
            raise ValueError(
                "A document with this filename already exists."
            )

        stored_filename = (
            f"{uuid.uuid4()}{extension}"
        )

        storage_path = (
            UPLOAD_DIRECTORY
            / stored_filename
        )

        with open(
            storage_path,
            "wb",
        ) as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

        document = Document(
            knowledge_base_id=knowledge_base_id,
            original_filename=file.filename,
            stored_filename=stored_filename,
            storage_path=str(storage_path),
            content_type=file.content_type
            or "application/pdf",
            file_size=storage_path.stat().st_size,
            status=DocumentStatus.UPLOADED,
        )

        await self.uow.documents.create(
            document,
        )

        await self.uow.commit()

        # Run document processing asynchronously in background
        import asyncio
        asyncio.create_task(self._bg_process(document.id))

        return document

    async def _bg_process(self, document_id: int) -> None:
        async with UnitOfWork() as bg_uow:
            doc = await bg_uow.documents.get_by_id(document_id)
            if doc:
                await self.processor.process(document=doc, uow=bg_uow)

    async def list_documents(
        self,
        knowledge_base_id: int,
    ) -> list[Document]:

        knowledge_base = (
            await self.uow.knowledge_bases.get_by_id(
                knowledge_base_id,
            )
        )

        if knowledge_base is None:
            raise ValueError(
                "Knowledge Base not found."
            )

        return (
            await self.uow.documents.list_by_knowledge_base(
                knowledge_base_id,
            )
        )

    async def get_document(
        self,
        document_id: int,
    ) -> Document:

        document = (
            await self.uow.documents.get_by_id(
                document_id,
            )
        )

        if document is None:
            raise ValueError(
                "Document not found."
            )

        return document

    async def delete_document(
        self,
        document_id: int,
    ) -> None:

        document = (
            await self.uow.documents.get_by_id(
                document_id,
            )
        )

        if document is None:
            raise ValueError(
                "Document not found."
            )

        storage_path = Path(
            document.storage_path,
        )

        if storage_path.exists():
            storage_path.unlink()

        await self.uow.document_chunks.delete_by_document(
            document.id,
        )

        await self.uow.documents.delete(
            document,
        )

        await self.uow.commit()