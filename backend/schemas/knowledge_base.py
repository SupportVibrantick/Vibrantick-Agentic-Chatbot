from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from models.knowledge_base import KnowledgeBaseStatus


class KnowledgeBaseCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=150,
    )
    description: str | None = None

    embedding_provider: str = Field(
        default="bge",
        max_length=100,
    )

    embedding_model: str = Field(
        default="BAAI/bge-m3",
        max_length=150,
    )

    chunk_size: int = Field(
        default=1000,
        ge=100,
        le=4000,
    )

    chunk_overlap: int = Field(
        default=200,
        ge=0,
        le=1000,
    )


class KnowledgeBaseUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=150,
    )

    description: str | None = None

    status: KnowledgeBaseStatus | None = None

    embedding_provider: str | None = Field(
        default=None,
        max_length=100,
    )

    embedding_model: str | None = Field(
        default=None,
        max_length=150,
    )

    chunk_size: int | None = Field(
        default=None,
        ge=100,
        le=4000,
    )

    chunk_overlap: int | None = Field(
        default=None,
        ge=0,
        le=1000,
    )

    is_active: bool | None = None


class KnowledgeBaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    chatbot_id: int

    name: str
    description: str | None

    status: KnowledgeBaseStatus

    embedding_provider: str
    embedding_model: str

    chunk_size: int
    chunk_overlap: int

    is_active: bool

    last_indexed_at: datetime | None

    created_at: datetime
    updated_at: datetime


class KnowledgeBaseListResponse(BaseModel):
    items: list[KnowledgeBaseResponse]
    total: int