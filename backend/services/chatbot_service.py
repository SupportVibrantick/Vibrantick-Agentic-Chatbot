import re
from uuid import uuid4

from database.unit_of_work import UnitOfWork
from models.chatbot import Chatbot, ChatbotStatus


class ChatbotService:
    """
    Business logic for chatbot management.
    """

    def __init__(
        self,
        uow: UnitOfWork,
    ) -> None:
        self.uow = uow

    async def _generate_slug(
        self,
        organization_id: int,
        name: str,
    ) -> str:
        """
        Generate a unique slug within an organization.
        """

        slug = name.lower().strip()
        slug = re.sub(r"[^a-z0-9]+", "-", slug)
        slug = slug.strip("-")

        original_slug = slug
        counter = 1

        while await self.uow.chatbots.exists_by_slug(
            organization_id,
            slug,
        ):
            slug = f"{original_slug}-{counter}"
            counter += 1

        return slug

    async def create_chatbot(
        self,
        *,
        organization_id: int,
        created_by: int,
        name: str,
        description: str | None = None,
        avatar: str | None = None,
        welcome_message: str | None = None,
        placeholder_text: str | None = None,
        is_public: bool = False,
    ) -> Chatbot:

        organization = await self.uow.organizations.get_by_id(
            organization_id
        )

        if organization is None:
            raise ValueError("Organization not found.")

        slug = await self._generate_slug(
            organization_id,
            name,
        )

        chatbot = Chatbot(
            organization_id=organization_id,
            created_by=created_by,
            name=name,
            slug=slug,
            description=description,
            avatar=avatar,
            welcome_message=welcome_message,
            placeholder_text=placeholder_text,
            is_public=is_public,
            public_uuid=str(uuid4()),
            status=ChatbotStatus.DRAFT,
        )

        await self.uow.chatbots.add(chatbot)

        await self.uow.flush()

        await self.uow.refresh(chatbot)

        await self.uow.commit()

        return chatbot

    async def get_chatbot(
        self,
        chatbot_id: int,
    ) -> Chatbot | None:
        return await self.uow.chatbots.get_by_id(chatbot_id)

    async def list_chatbots(
        self,
        organization_id: int,
    ) -> list[Chatbot]:
        return await self.uow.chatbots.list_by_organization(
            organization_id
        )

    async def delete_chatbot(
        self,
        chatbot: Chatbot,
    ) -> None:
        await self.uow.chatbots.delete(chatbot)
        await self.uow.commit()