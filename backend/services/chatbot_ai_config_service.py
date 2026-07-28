from __future__ import annotations

from database.unit_of_work import UnitOfWork
from models.chatbot_ai_config import ChatbotAIConfig
from schemas.chatbot_ai_config import (
    ChatbotAIConfigCreate,
    ChatbotAIConfigUpdate,
)


class ChatbotAIConfigService:
    """
    Business logic for chatbot AI configuration.
    """

    async def create_config(
        self,
        chatbot_id: int,
        data: ChatbotAIConfigCreate,
        uow: UnitOfWork,
    ) -> ChatbotAIConfig:
        chatbot = await uow.chatbots.get_by_id(chatbot_id)

        if chatbot is None:
            raise ValueError("Chatbot not found.")

        existing = await uow.chatbot_ai_configs.get_by_chatbot_id(
            chatbot_id
        )

        if existing is not None:
            raise ValueError(
                "AI configuration already exists for this chatbot."
            )

        config = ChatbotAIConfig(
            chatbot_id=chatbot_id,
            provider=data.provider,
            model_name=data.model_name,
            system_prompt=data.system_prompt,
            temperature=data.temperature,
            max_tokens=data.max_tokens,
            streaming=data.streaming,
        )

        await uow.chatbot_ai_configs.add(config)
        await uow.flush()
        await uow.refresh(config)
        await uow.commit()

        return config

    async def get_config(
        self,
        chatbot_id: int,
        uow: UnitOfWork,
    ) -> ChatbotAIConfig | None:
        return await uow.chatbot_ai_configs.get_by_chatbot_id(
            chatbot_id
        )

    async def update_config(
        self,
        chatbot_id: int,
        data: ChatbotAIConfigUpdate,
        uow: UnitOfWork,
    ) -> ChatbotAIConfig:
        config = await uow.chatbot_ai_configs.get_by_chatbot_id(
            chatbot_id
        )

        if config is None:
            raise ValueError("AI configuration not found.")

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(config, field, value)

        await uow.flush()
        await uow.refresh(config)
        await uow.commit()

        return config

    async def delete_config(
        self,
        chatbot_id: int,
        uow: UnitOfWork,
    ) -> None:
        config = await uow.chatbot_ai_configs.get_by_chatbot_id(
            chatbot_id
        )

        if config is None:
            raise ValueError("AI configuration not found.")

        await uow.chatbot_ai_configs.delete(config)
        await uow.commit()