from __future__ import annotations

import hashlib
from pathlib import Path

from database.unit_of_work import UnitOfWork
from models.document import Document, DocumentStatus
from models.knowledge_source import (
    KnowledgeSource,
    KnowledgeSourceStatus,
    KnowledgeSourceType,
)
from services.document_processing.ingestion_service import (
    IngestionService,
)
from services.storage import LocalStorage


class KnowledgeSourceService:
    """
    Handles uploaded knowledge sources and creates the
    corresponding Document used by the ingestion pipeline.
    """

    def __init__(
        self,
        uow: UnitOfWork,
        storage: LocalStorage | None = None,
    ) -> None:
        self.uow = uow
        self.storage = storage or LocalStorage()

    async def upload_file(
        self,
        *,
        knowledge_base_id: int,
        filename: str,
        content: bytes,
        content_type: str,
    ) -> KnowledgeSource:
        knowledge_base = await self.uow.knowledge_bases.get_by_id(
            knowledge_base_id
        )

        if knowledge_base is None:
            raise ValueError("Knowledge base not found.")

        suffix = Path(filename).suffix.lower()

        file_type_map = {
            ".pdf": KnowledgeSourceType.PDF,
            ".docx": KnowledgeSourceType.DOCX,
            ".txt": KnowledgeSourceType.TXT,
            ".csv": KnowledgeSourceType.CSV,
            ".html": KnowledgeSourceType.HTML,
            ".md": KnowledgeSourceType.MARKDOWN,
        }

        if suffix not in file_type_map:
            raise ValueError("Unsupported file type.")

        checksum = hashlib.sha256(content).hexdigest()

        storage_metadata = self.storage.save_bytes(
            filename=filename,
            content=content,
            content_type=content_type,
        )
        storage_path = storage_metadata["file_path"]
        # ---------------------------------------------------------
        # 1. Create KnowledgeSource
        # ---------------------------------------------------------
        source = KnowledgeSource(
            knowledge_base_id=knowledge_base_id,
            name=filename,
            source_type=file_type_map[suffix],
            status=KnowledgeSourceStatus.PENDING,
            file_name=filename,
            file_path=storage_path,
            mime_type=content_type,
            file_size=len(content),
            checksum=checksum,
        )

        await self.uow.knowledge_sources.add(source)
        await self.uow.flush()
        await self.uow.refresh(source)

        # ---------------------------------------------------------
        # 2. Create actual Document
        # ---------------------------------------------------------
        document = Document(
            knowledge_base_id=knowledge_base_id,
            original_filename=filename,
            stored_filename=Path(storage_path).name,
            storage_path=storage_path,
            content_type=content_type,
            file_size=len(content),
            status=DocumentStatus.UPLOADED,
        )

        await self.uow.documents.add(document)
        await self.uow.flush()
        await self.uow.refresh(document)

        # ---------------------------------------------------------
        # 3. Process Document
        # ---------------------------------------------------------
        ingestion = IngestionService()

        await ingestion.ingest(
            document=document,
            knowledge_source=source,
            uow=self.uow,
        )

        await self.uow.refresh(source)

        return source