from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from models.chatbot_ai_config import LLMProvider


class ChatbotAIConfigBase(BaseModel):
    provider: LLMProvider
    model_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )
    system_prompt: str = Field(
        ...,
        min_length=1,
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
    )
    max_tokens: int = Field(
        default=2048,
        ge=1,
    )
    streaming: bool = False


class ChatbotAIConfigCreate(ChatbotAIConfigBase):
    pass


class ChatbotAIConfigUpdate(BaseModel):
    provider: LLMProvider | None = None
    model_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    system_prompt: str | None = Field(
        default=None,
        min_length=1,
    )
    temperature: float | None = Field(
        default=None,
        ge=0.0,
        le=2.0,
    )
    max_tokens: int | None = Field(
        default=None,
        ge=1,
    )
    streaming: bool | None = None


class ChatbotAIConfigResponse(ChatbotAIConfigBase):
    id: int
    chatbot_id: int

    model_config = ConfigDict(
        from_attributes=True,
    )