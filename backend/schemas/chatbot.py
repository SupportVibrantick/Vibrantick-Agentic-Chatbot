from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from models.chatbot import ChatbotStatus


# ==========================================================
# Base
# ==========================================================

class ChatbotBase(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
        max_length=1000,
    )

    avatar: str | None = None

    welcome_message: str | None = Field(
        default=None,
        max_length=1000,
    )

    placeholder_text: str | None = Field(
        default=None,
        max_length=255,
    )

    is_public: bool = False


# ==========================================================
# Create
# ==========================================================

class ChatbotCreate(ChatbotBase):
    pass


# ==========================================================
# Update
# ==========================================================

class ChatbotUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
        max_length=1000,
    )

    avatar: str | None = None

    welcome_message: str | None = Field(
        default=None,
        max_length=1000,
    )

    placeholder_text: str | None = Field(
        default=None,
        max_length=255,
    )

    is_public: bool | None = None


# ==========================================================
# Response
# ==========================================================

class ChatbotResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    organization_id: int

    created_by: int

    name: str

    slug: str

    description: str | None

    avatar: str | None

    welcome_message: str | None

    placeholder_text: str | None

    status: ChatbotStatus

    is_public: bool

    public_uuid: str

    last_trained_at: datetime | None

    created_at: datetime

    updated_at: datetime


# ==========================================================
# List Response
# ==========================================================

class ChatbotListResponse(BaseModel):
    items: list[ChatbotResponse]
    total: int