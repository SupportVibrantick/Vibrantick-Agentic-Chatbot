from __future__ import annotations

from database.unit_of_work import UnitOfWork

from models.knowledge_base import KnowledgeBase

from schemas.knowledge_base import (
    KnowledgeBaseCreate,
    KnowledgeBaseUpdate,
)


class KnowledgeBaseService:
    """
    Handles Knowledge Base business logic.
    """

    async def create(
        self,
        chatbot_id: int,
        data: KnowledgeBaseCreate,
        uow: UnitOfWork,
    ) -> KnowledgeBase:
        chatbot = await uow.chatbots.get_by_id(chatbot_id)

        if chatbot is None:
            raise ValueError("Chatbot not found.")

        if await uow.knowledge_bases.exists_by_name(
            chatbot_id=chatbot_id,
            name=data.name,
        ):
            raise ValueError(
                "Knowledge Base already exists."
            )

        knowledge_base = KnowledgeBase(
            chatbot_id=chatbot_id,
            **data.model_dump(),
        )

        await uow.knowledge_bases.add(
            knowledge_base,
        )

        await uow.flush()
        await uow.refresh(
            knowledge_base,
        )

        return knowledge_base

    async def get_by_id(
        self,
        knowledge_base_id: int,
        uow: UnitOfWork,
    ) -> KnowledgeBase | None:
        return await uow.knowledge_bases.get_by_id(
            knowledge_base_id,
        )

    async def list_by_chatbot(
        self,
        chatbot_id: int,
        uow: UnitOfWork,
    ) -> list[KnowledgeBase]:
        return await uow.knowledge_bases.list_by_chatbot(
            chatbot_id,
        )

    async def update(
        self,
        knowledge_base: KnowledgeBase,
        data: KnowledgeBaseUpdate,
        uow: UnitOfWork,
    ) -> KnowledgeBase:
        updates = data.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )

        for field, value in updates.items():
            setattr(
                knowledge_base,
                field,
                value,
            )

        await uow.flush()
        await uow.refresh(
            knowledge_base,
        )
        await uow.commit()

        return knowledge_base

    async def delete(
        self,
        knowledge_base: KnowledgeBase,
        uow: UnitOfWork,
    ) -> None:
        await uow.knowledge_bases.delete(
            knowledge_base,
        )
        await uow.commit()