
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.message import Message
from repositories.base_repository import BaseRepository


class MessageRepository(BaseRepository[Message]):
    model = Message

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        super().__init__(session)

    async def list_by_conversation(
        self,
        conversation_id: int,
        limit: int = 50,
    ) -> list[Message]:
        stmt = (
            select(Message)
            .where(
                Message.conversation_id == conversation_id,
            )
            .order_by(
                Message.created_at.asc(),
            )
            .limit(limit)
        )

        result = await self.session.execute(stmt)

        return list(result.scalars().all())