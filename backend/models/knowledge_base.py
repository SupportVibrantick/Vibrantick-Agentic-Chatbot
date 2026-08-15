from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
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


class KnowledgeBaseStatus(str, Enum):
    DRAFT = "draft"
    INDEXING = "indexing"
    READY = "ready"
    FAILED = "failed"
    ARCHIVED = "archived"


if TYPE_CHECKING:
    from models.chatbot import Chatbot
    from models.document import Document
    from models.knowledge_source import KnowledgeSource


class KnowledgeBase(TimestampMixin, Base):
    __tablename__ = "knowledge_bases"

    __table_args__ = (
        UniqueConstraint(
            "chatbot_id",
            "name",
            name="uq_chatbot_knowledge_base_name",
        ),
        Index("ix_kb_chatbot", "chatbot_id"),
        Index("ix_kb_status", "status"),
        Index("ix_kb_active", "is_active"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    chatbot_id: Mapped[int] = mapped_column(
        ForeignKey(
            "chatbots.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[KnowledgeBaseStatus] = mapped_column(
        SQLEnum(KnowledgeBaseStatus),
        default=KnowledgeBaseStatus.DRAFT,
        nullable=False,
    )

    embedding_provider: Mapped[str] = mapped_column(
        String(100),
        default="bge",
        nullable=False,
    )

    embedding_model: Mapped[str] = mapped_column(
        String(150),
        default="BAAI/bge-m3",
        nullable=False,
    )

    chunk_size: Mapped[int] = mapped_column(
        default=1000,
        nullable=False,
    )

    chunk_overlap: Mapped[int] = mapped_column(
        default=200,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    last_indexed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    chatbot: Mapped["Chatbot"] = relationship(
        "Chatbot",
        back_populates="knowledge_bases",
        lazy="selectin",
    )

    documents: Mapped[list["Document"]] = relationship(
        "Document",
        back_populates="knowledge_base",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="selectin",
    )

    knowledge_sources: Mapped[list["KnowledgeSource"]] = relationship(
        "KnowledgeSource",
        back_populates="knowledge_base",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="selectin",
    )