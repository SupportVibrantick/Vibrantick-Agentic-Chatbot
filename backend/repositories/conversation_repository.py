from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.conversation import Conversation
from repositories.base_repository import BaseRepository


class ConversationRepository(
    BaseRepository[Conversation]
):
    model = Conversation

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        super().__init__(session)

    async def get_by_id(
        self,
        conversation_id: int,
    ) -> Conversation | None:
        stmt = (
            select(Conversation)
            .where(
                Conversation.id == conversation_id,
            )
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def list_by_chatbot(
        self,
        chatbot_id: int,
    ) -> list[Conversation]:
        stmt = (
            select(Conversation)
            .where(
                Conversation.chatbot_id == chatbot_id,
            )
            .order_by(
                Conversation.updated_at.desc(),
            )
        )

        result = await self.session.execute(stmt)

        return list(result.scalars().all())