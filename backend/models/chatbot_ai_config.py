from enum import Enum

from sqlalchemy import Boolean, Enum as SQLEnum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base
from models.base import TimestampMixin


class LLMProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    OLLAMA = "ollama"


class ChatbotAIConfig(Base, TimestampMixin):
    __tablename__ = "chatbot_ai_configs"

    id: Mapped[int] = mapped_column(primary_key=True)

    chatbot_id: Mapped[int] = mapped_column(
        ForeignKey("chatbots.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    provider: Mapped[LLMProvider] = mapped_column(
        SQLEnum(LLMProvider),
        default=LLMProvider.OPENAI,
    )

    model_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="gpt-4.1",
    )

    system_prompt: Mapped[str] = mapped_column(
        Text,
        default="You are a helpful AI assistant.",
    )

    temperature: Mapped[float] = mapped_column(
        Float,
        default=0.7,
    )

    max_tokens: Mapped[int] = mapped_column(
        Integer,
        default=2048,
    )

    streaming: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    chatbot = relationship(
        "Chatbot",
        back_populates="ai_config",
    )