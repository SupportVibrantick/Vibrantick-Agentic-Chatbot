from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import (
    Enum as SQLEnum,
    ForeignKey,
    Index,
    Integer,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base
from models.base import TimestampMixin

if TYPE_CHECKING:
    from models.conversation import Conversation


class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class Message(TimestampMixin, Base):
    __tablename__ = "messages"

    __table_args__ = (
        Index("ix_message_conversation", "conversation_id"),
        Index("ix_message_role", "role"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    conversation_id: Mapped[int] = mapped_column(
        ForeignKey(
            "conversations.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    role: Mapped[MessageRole] = mapped_column(
        SQLEnum(MessageRole),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    token_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    conversation: Mapped["Conversation"] = relationship(
        "Conversation",
        back_populates="messages",
    )