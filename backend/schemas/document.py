from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from models.document import DocumentStatus


class DocumentResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    knowledge_base_id: int

    original_filename: str
    stored_filename: str

    storage_path: str

    content_type: str

    file_size: int

    status: DocumentStatus

    created_at: datetime
    updated_at: datetime


class DocumentListResponse(BaseModel):
    items: list[DocumentResponse]
    total: int