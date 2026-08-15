from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.knowledge_base import KnowledgeBase
from repositories.base_repository import BaseRepository


class KnowledgeBaseRepository(BaseRepository[KnowledgeBase]):
    model = KnowledgeBase

    def __init__(
        self,
        session: AsyncSession,
    ):
        super().__init__(session)

    async def get_by_chatbot(
        self,
        chatbot_id: int,
    ) -> KnowledgeBase | None:
        stmt = (
            select(KnowledgeBase)
            .where(
                KnowledgeBase.chatbot_id == chatbot_id,
                KnowledgeBase.is_active.is_(True),
            )
            .limit(1)
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def list_by_chatbot(
        self,
        chatbot_id: int,
    ) -> list[KnowledgeBase]:
        stmt = (
            select(KnowledgeBase)
            .where(
                KnowledgeBase.chatbot_id == chatbot_id,
            )
            .order_by(
                KnowledgeBase.created_at.desc(),
            )
        )

        result = await self.session.execute(stmt)

        return list(result.scalars().all())

    async def get_by_name(
        self,
        chatbot_id: int,
        name: str,
    ) -> KnowledgeBase | None:
        stmt = (
            select(KnowledgeBase)
            .where(
                KnowledgeBase.chatbot_id == chatbot_id,
                KnowledgeBase.name == name,
            )
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def exists_by_name(
        self,
        chatbot_id: int,
        name: str,
    ) -> bool:
        return (
            await self.get_by_name(
                chatbot_id,
                name,
            )
            is not None
        )

    async def list_active(
        self,
        chatbot_id: int,
    ) -> list[KnowledgeBase]:
        stmt = (
            select(KnowledgeBase)
            .where(
                KnowledgeBase.chatbot_id == chatbot_id,
                KnowledgeBase.is_active.is_(True),
            )
            .order_by(
                KnowledgeBase.name,
            )
        )

        result = await self.session.execute(stmt)

        return list(result.scalars().all())

    async def get_active_by_id(
        self,
        knowledge_base_id: int,
    ) -> KnowledgeBase | None:
        stmt = (
            select(KnowledgeBase)
            .where(
                KnowledgeBase.id == knowledge_base_id,
                KnowledgeBase.is_active.is_(True),
            )
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()