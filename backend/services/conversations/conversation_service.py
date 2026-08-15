from __future__ import annotations

from database.unit_of_work import UnitOfWork

from services.llm.provider_factory import ProviderFactory
from services.llm.types import (
    LLMMessage,
    LLMRequest,
    MessageRole,
)

from services.retrieval.context_builder import ContextBuilder
from services.retrieval.vector_search_service import VectorSearchService


class ConversationService:
    """
    Handles chatbot conversations using Retrieval-Augmented Generation (RAG).
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
        # Retrieve knowledge base context
        # -----------------------------------------------------

        context = ""

        knowledge_bases = await uow.knowledge_bases.list_active(
            chatbot_id
        )

        if knowledge_bases:

            vector_search = VectorSearchService(
                uow.session,
            )

            context_builder = ContextBuilder()

            chunks = await vector_search.search(
                query=message,
                knowledge_base_id=knowledge_bases[0].id,
                embedding_model=getattr(
                    config,
                    "embedding_model",
                    "text-embedding-3-small",
                ),
                top_k=getattr(
                    config,
                    "top_k",
                    5,
                ),
            )

            context = context_builder.build(
                chunks,
            )

        # -----------------------------------------------------
        # Build system prompt
        # -----------------------------------------------------

        system_prompt = config.system_prompt

        if context:
            system_prompt += (
                "\n\n"
                "Use ONLY the information below when it is relevant.\n"
                "If the answer is not contained in the context, "
                "say that you don't know instead of making up facts.\n\n"
                "Knowledge Base Context:\n"
                f"{context}"
            )

        # -----------------------------------------------------
        # Build LLM request
        # -----------------------------------------------------

        request = LLMRequest(
            model=config.model_name,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            messages=[
                LLMMessage(
                    role=MessageRole.SYSTEM,
                    content=system_prompt,
                ),
                LLMMessage(
                    role=MessageRole.USER,
                    content=message,
                ),
            ],
        )

        # -----------------------------------------------------
        # Generate response
        # -----------------------------------------------------

        provider = ProviderFactory.create(
            config.provider,
        )

        response = await provider.generate(
            request,
        )

        return response.content