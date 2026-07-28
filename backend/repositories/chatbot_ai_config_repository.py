from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.chatbot_ai_config import ChatbotAIConfig
from repositories.base_repository import BaseRepository


class ChatbotAIConfigRepository(
    BaseRepository[ChatbotAIConfig]
):
    """
    Repository for ChatbotAIConfig persistence.
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        super().__init__(
            session=session,
            model=ChatbotAIConfig,
        )

    async def get_by_chatbot_id(
        self,
        chatbot_id: int,
    ) -> ChatbotAIConfig | None:
        """
        Return AI configuration for a chatbot.
        """

        stmt = (
            select(ChatbotAIConfig)
            .where(
                ChatbotAIConfig.chatbot_id == chatbot_id
            )
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()