from typing import TYPE_CHECKING
from datetime import datetime
from enum import Enum
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

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from database.base import Base
from models.base import TimestampMixin


class ChatbotStatus(str, Enum):
    DRAFT = "draft"
    TRAINING = "training"
    READY = "ready"
    PAUSED = "paused"
    ARCHIVED = "archived"


if TYPE_CHECKING:
    from models.conversation import Conversation
    from models.knowledge_base import KnowledgeBase
    
class Chatbot(TimestampMixin, Base):
    __tablename__ = "chatbots"

    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "slug",
            name="uq_chatbot_org_slug",
        ),
        Index("ix_chatbot_organization", "organization_id"),
        Index("ix_chatbot_status", "status"),
        Index("ix_chatbot_public_uuid", "public_uuid"),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    organization_id: Mapped[int] = mapped_column(
        ForeignKey(
            "organizations.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    created_by: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    slug: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[ChatbotStatus] = mapped_column(
        SQLEnum(ChatbotStatus),
        default=ChatbotStatus.DRAFT,
        nullable=False,
    )

    avatar: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    welcome_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    placeholder_text: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    is_public: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    public_uuid: Mapped[str | None] = mapped_column(
        String(64),
        unique=True,
        nullable=True,
    )

    last_trained_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    organization: Mapped["Organization"] = relationship(
        "Organization",
        back_populates="chatbots",
    )

    creator: Mapped["User"] = relationship(
        "User",
        foreign_keys=[created_by],
        back_populates="created_chatbots",
    )
    ai_config: Mapped["ChatbotAIConfig"] = relationship(
        "ChatbotAIConfig",
        back_populates="chatbot",
        uselist=False,
        cascade="all, delete-orphan",
    )

    conversations: Mapped[list["Conversation"]] = relationship(
        "Conversation",
        back_populates="chatbot",
        cascade="all, delete-orphan",
    )
    
    knowledge_bases: Mapped[list["KnowledgeBase"]] = relationship(
        "KnowledgeBase",
        back_populates="chatbot",
        cascade="all, delete-orphan",
    )