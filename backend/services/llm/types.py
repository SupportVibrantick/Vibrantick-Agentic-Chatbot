from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass(slots=True)
class LLMMessage:
    role: MessageRole
    content: str


@dataclass(slots=True)
class LLMRequest:
    messages: list[LLMMessage]
    temperature: float = 0.7
    max_tokens: int = 2048