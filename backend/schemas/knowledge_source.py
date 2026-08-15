from datetime import datetime

from pydantic import BaseModel, ConfigDict

from models.knowledge_source import (
    KnowledgeSourceStatus,
    KnowledgeSourceType,
)


class KnowledgeSourceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    knowledge_base_id: int

    name: str

    source_type: KnowledgeSourceType
    status: KnowledgeSourceStatus

    file_name: str | None
    file_path: str | None
    mime_type: str | None
    file_size: int | None
    checksum: str | None

    created_at: datetime
    updated_at: datetime


class KnowledgeSourceListResponse(BaseModel):
    items: list[KnowledgeSourceResponse]
    total: int