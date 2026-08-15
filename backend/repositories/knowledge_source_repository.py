from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.document import Document
from repositories.base_repository import BaseRepository


class KnowledgeSourceRepository(BaseRepository[KnowledgeSource]):
    model = KnowledgeSource

    def __init__(
        self,
        session: AsyncSession,
    ):
        super().__init__(session)

    async def list_by_knowledge_base(
        self,
        knowledge_base_id: int,
    ) -> list[KnowledgeSource]:
        stmt = (
            select(KnowledgeSource)
            .where(
                KnowledgeSource.knowledge_base_id == knowledge_base_id,
            )
            .order_by(KnowledgeSource.created_at.desc())
        )

        result = await self.session.execute(stmt)

        return list(result.scalars().all())

    async def get_by_name(
        self,
        knowledge_base_id: int,
        name: str,
    ) -> KnowledgeSource | None:
        stmt = (
            select(KnowledgeSource)
            .where(
                KnowledgeSource.knowledge_base_id == knowledge_base_id,
                KnowledgeSource.name == name,
            )
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def exists_by_name(
        self,
        knowledge_base_id: int,
        name: str,
    ) -> bool:
        return (
            await self.get_by_name(
                knowledge_base_id,
                name,
            )
            is not None
        )