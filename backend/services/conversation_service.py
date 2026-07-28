from __future__ import annotations

from database.unit_of_work import UnitOfWork
from services.llm.provider_factory import ProviderFactory
from services.llm.types import (
    LLMMessage,
    LLMRequest,
    MessageRole,
)


class ConversationService:
    """
    Handles chatbot conversations.
    """

    async def chat(
        self,
        chatbot_id: int,
        message: str,
        uow: UnitOfWork,
    ) -> str:
        # -----------------------------------------------------
        # Load chatbot
        # -----------------------------------------------------

        chatbot = await uow.chatbots.get_by_id(chatbot_id)

        if chatbot is None:
            raise ValueError("Chatbot not found.")

        # -----------------------------------------------------
        # Load AI configuration
        # -----------------------------------------------------

        config = await uow.chatbot_ai_configs.get_by_chatbot_id(
            chatbot_id
        )

        if config is None:
            raise ValueError(
                "AI configuration not found."
            )

        # -----------------------------------------------------
        # Build request
        # -----------------------------------------------------

        request = LLMRequest(
            model=config.model_name,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            messages=[
                LLMMessage(
                    role=MessageRole.SYSTEM,
                    content=config.system_prompt,
                ),
                LLMMessage(
                    role=MessageRole.USER,
                    content=message,
                ),
            ],
        )

        # -----------------------------------------------------
        # Create provider
        # -----------------------------------------------------

        provider = ProviderFactory.create(
            config.provider
        )

        # -----------------------------------------------------
        # Generate response
        # -----------------------------------------------------

        response = await provider.generate(
            request
        )

        return response.content