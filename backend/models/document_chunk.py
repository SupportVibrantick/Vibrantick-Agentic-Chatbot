from __future__ import annotations

from typing import TYPE_CHECKING

from pgvector.sqlalchemy import Vector

from sqlalchemy import (
    ForeignKey,
    Index,
    Integer,
    JSON,
    Text,
    UniqueConstraint,
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base
from models.base import TimestampMixin


if TYPE_CHECKING:
    from models.document import Document


class DocumentChunk(TimestampMixin, Base):
    __tablename__ = "document_chunks"

    __table_args__ = (
        Index(
            "ix_document_chunk_document",
            "document_id",
        ),
        UniqueConstraint(
            "document_id",
            "chunk_index",
            name="uq_document_chunk_index",
        ),
        Index(
            "ix_document_chunks_embedding_hnsw",
            "embedding",
            postgresql_using="hnsw",
            postgresql_ops={
                "embedding": "vector_cosine_ops",
            },
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    document_id: Mapped[int] = mapped_column(
        ForeignKey(
            "documents.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    token_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    # Python attribute is metadata_ because "metadata" is reserved
    # by SQLAlchemy's Declarative API.
    #
    # Database column remains exactly:
    #     document_chunks.metadata
    metadata_: Mapped[dict | None] = mapped_column(
        "metadata",
        JSON,
        nullable=True,
    )

    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(1024),
        nullable=True,
    )

    document: Mapped["Document"] = relationship(
        "Document",
        back_populates="chunks",
    )