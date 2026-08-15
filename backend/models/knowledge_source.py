from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Index,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base
from models.base import TimestampMixin
if TYPE_CHECKING:
    from models.document_chunk import DocumentChunk
    document_chunks: Mapped[list["DocumentChunk"]] = relationship(
    "DocumentChunk",
    back_populates="knowledge_source",
    cascade="all, delete-orphan",
    passive_deletes=True,
    lazy="selectin",
    )

class KnowledgeSourceType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    CSV = "csv"
    HTML = "html"
    MARKDOWN = "markdown"
    WEBSITE = "website"
    NOTION = "notion"
    CONFLUENCE = "confluence"
    DATABASE = "database"
    S3 = "s3"


class KnowledgeSourceStatus(str, Enum):
    PENDING = "pending"
    UPLOADING = "uploading"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"
    DELETED = "deleted"


if TYPE_CHECKING:
    from models.knowledge_base import KnowledgeBase
    from models.document_chunk import DocumentChunk


class KnowledgeSource(TimestampMixin, Base):
    __tablename__ = "knowledge_sources"

    __table_args__ = (
        UniqueConstraint(
            "knowledge_base_id",
            "name",
            name="uq_kb_source_name",
        ),
        Index("ix_knowledge_source_kb", "knowledge_base_id"),
        Index("ix_knowledge_source_status", "status"),
        Index("ix_knowledge_source_type", "source_type"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    knowledge_base_id: Mapped[int] = mapped_column(
        ForeignKey("knowledge_bases.id", ondelete="CASCADE"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    source_type: Mapped[KnowledgeSourceType] = mapped_column(
        SQLEnum(KnowledgeSourceType),
        nullable=False,
    )

    status: Mapped[KnowledgeSourceStatus] = mapped_column(
        SQLEnum(KnowledgeSourceStatus),
        default=KnowledgeSourceStatus.PENDING,
        nullable=False,
    )

    file_name: Mapped[str | None] = mapped_column(String(255))
    file_path: Mapped[str | None] = mapped_column(String(1000))
    mime_type: Mapped[str | None] = mapped_column(String(150))
    file_size: Mapped[int | None] = mapped_column(BigInteger)
    checksum: Mapped[str | None] = mapped_column(String(64))
    source_url: Mapped[str | None] = mapped_column(String(2048))
    error_message: Mapped[str | None] = mapped_column(Text)

    processed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )

    knowledge_base: Mapped["KnowledgeBase"] = relationship(
        "KnowledgeBase",
        back_populates="documents",
        lazy="selectin",
    )

    document_chunks: Mapped[list["DocumentChunk"]] = relationship(
        "DocumentChunk",
        back_populates="knowledge_source",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="selectin",
    )