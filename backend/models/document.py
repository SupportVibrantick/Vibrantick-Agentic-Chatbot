from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import (
    Enum as SQLEnum,
    ForeignKey,
    Index,
    Integer,
    BigInteger,
    String,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from database.base import Base
from models.base import TimestampMixin

if TYPE_CHECKING:
    from models.knowledge_base import KnowledgeBase
    from models.document_chunk import DocumentChunk


class DocumentStatus(str, Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"


class Document(TimestampMixin, Base):
    __tablename__ = "documents"

    __table_args__ = (
        Index("ix_document_knowledge_base", "knowledge_base_id"),
        Index("ix_document_status", "status"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    knowledge_base_id: Mapped[int] = mapped_column(
        ForeignKey(
            "knowledge_bases.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    original_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    stored_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    storage_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    content_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    file_size: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    status: Mapped[DocumentStatus] = mapped_column(
        SQLEnum(DocumentStatus),
        default=DocumentStatus.UPLOADED,
        nullable=False,
    )

    knowledge_base: Mapped["KnowledgeBase"] = relationship(
        "KnowledgeBase",
        back_populates="documents",
        lazy="selectin",
    )

    chunks: Mapped[list["DocumentChunk"]] = relationship(
        "DocumentChunk",
        back_populates="document",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="selectin",
    )