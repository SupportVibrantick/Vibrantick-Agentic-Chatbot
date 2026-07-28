from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.chatbot import Chatbot
from repositories.base_repository import BaseRepository

class ChatbotRepository(BaseRepository[Chatbot]):
    model = Chatbot

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_by_slug(
        self,
        organization_id: int,
        slug: str,
    ) -> Chatbot | None:
        stmt = (
            select(Chatbot)
            .where(
                Chatbot.organization_id == organization_id,
                Chatbot.slug == slug,
            )
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_organization(
        self,
        organization_id: int,
    ) -> list[Chatbot]:
        stmt = (
            select(Chatbot)
            .where(Chatbot.organization_id == organization_id)
            .order_by(Chatbot.created_at.desc())
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def exists_by_slug(
        self,
        organization_id: int,
        slug: str,
    ) -> bool:
        chatbot = await self.get_by_slug(
            organization_id,
            slug,
        )

        return chatbot is not None

    async def list_public_chatbots(self) -> list[Chatbot]:
        stmt = (
            select(Chatbot)
            .where(Chatbot.is_public.is_(True))
            .order_by(Chatbot.name)
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())