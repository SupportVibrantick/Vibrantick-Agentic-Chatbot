from __future__ import annotations

from collections.abc import AsyncIterator

from database.unit_of_work import UnitOfWork
from models.conversation import Conversation
from models.message import Message, MessageRole
from services.documents.retriever import DocumentRetriever
from services.llm.prompt_builder import PromptBuilder
from services.llm.provider_factory import ProviderFactory
from services.llm.types import (
    LLMMessage,
    LLMRequest,
    MessageRole as LLMMessageRole,
)


class ConversationService:
    """
    Handles chatbot conversations with multi-turn memory,
    RAG context, LLM interaction, and database persistence.
    """

    async def _get_or_create_conversation(
        self,
        chatbot_id: int,
        conversation_id: int | None,
        user_id: int | None,
        message: str,
        uow: UnitOfWork,
    ) -> Conversation:
        """
        Return an existing conversation only when it belongs
        to the requested chatbot.

        Otherwise create a new conversation.
        """
        if conversation_id is not None:
            conversation = await uow.conversations.get_by_id(
                conversation_id
            )

            if conversation is None:
                raise ValueError("Conversation not found.")

            if conversation.chatbot_id != chatbot_id:
                raise ValueError(
                    "Conversation does not belong to this chatbot."
                )

            return conversation

        title = message[:40] + (
            "..." if len(message) > 40 else ""
        )

        conversation = Conversation(
            chatbot_id=chatbot_id,
            title=title,
            created_by=user_id,
        )

        await uow.conversations.create(conversation)
        await uow.flush()

        return conversation

    async def _build_request(
        self,
        chatbot_id: int,
        conversation_id: int,
        message: str,
        uow: UnitOfWork,
    ) -> LLMRequest:
        """
        Build the LLM request using:
        - system instructions
        - conversation history
        - RAG context
        - current user message
        """
        context = ""

        knowledge_base = await uow.knowledge_bases.get_by_chatbot(
            chatbot_id
        )

        if knowledge_base:
            retriever = DocumentRetriever(uow)

            context = await retriever.retrieve(
                knowledge_base_id=knowledge_base.id,
                question=message,
            )

        messages_history = (
            await uow.messages.list_by_conversation(
                conversation_id=conversation_id,
                limit=20,
            )
        )

        llm_messages: list[LLMMessage] = [
            LLMMessage(
                role=LLMMessageRole.SYSTEM,
                content=(
                    "You are an intelligent enterprise AI assistant. "
                    "Answer questions accurately using the provided "
                    "knowledge base context when available."
                ),
            )
        ]

        for msg in messages_history:
            if msg.role == MessageRole.USER:
                role = LLMMessageRole.USER
            elif msg.role == MessageRole.ASSISTANT:
                role = LLMMessageRole.ASSISTANT
            else:
                role = LLMMessageRole.SYSTEM

            llm_messages.append(
                LLMMessage(
                    role=role,
                    content=msg.content,
                )
            )

        prompt_content = (
            PromptBuilder.build(
                context=context,
                question=message,
            )
            if context
            else message
        )

        llm_messages.append(
            LLMMessage(
                role=LLMMessageRole.USER,
                content=prompt_content,
            )
        )

        return LLMRequest(
            messages=llm_messages,
        )

    async def chat(
        self,
        chatbot_id: int,
        message: str,
        uow: UnitOfWork,
        conversation_id: int | None = None,
        user_id: int | None = None,
    ) -> dict[str, str | int]:
        """
        Execute a non-streaming chat request.
        """
        conversation = await self._get_or_create_conversation(
            chatbot_id=chatbot_id,
            conversation_id=conversation_id,
            user_id=user_id,
            message=message,
            uow=uow,
        )

        user_msg = Message(
            conversation_id=conversation.id,
            role=MessageRole.USER,
            content=message,
        )

        await uow.messages.create(user_msg)

        request = await self._build_request(
            chatbot_id=chatbot_id,
            conversation_id=conversation.id,
            message=message,
            uow=uow,
        )

        provider = ProviderFactory.create()

        response_text = await provider.chat(
            request
        )

        assistant_msg = Message(
            conversation_id=conversation.id,
            role=MessageRole.ASSISTANT,
            content=response_text,
        )

        await uow.messages.create(
            assistant_msg
        )

        await uow.commit()

        return {
            "conversation_id": conversation.id,
            "response": response_text,
        }

    async def stream_chat(
        self,
        chatbot_id: int,
        message: str,
        uow: UnitOfWork,
        conversation_id: int | None = None,
        user_id: int | None = None,
    ) -> AsyncIterator[str]:
        """
        Execute a streaming chat request.

        The assistant response is persisted only after
        the provider finishes streaming successfully.
        """
        conversation = await self._get_or_create_conversation(
            chatbot_id=chatbot_id,
            conversation_id=conversation_id,
            user_id=user_id,
            message=message,
            uow=uow,
        )

        user_msg = Message(
            conversation_id=conversation.id,
            role=MessageRole.USER,
            content=message,
        )

        await uow.messages.create(user_msg)
        await uow.flush()

        request = await self._build_request(
            chatbot_id=chatbot_id,
            conversation_id=conversation.id,
            message=message,
            uow=uow,
        )

        provider = ProviderFactory.create()

        full_response: list[str] = []

        async for token in provider.stream(
            request
        ):
            full_response.append(token)
            yield token

        response_text = "".join(
            full_response
        )

        assistant_msg = Message(
            conversation_id=conversation.id,
            role=MessageRole.ASSISTANT,
            content=response_text,
        )

        await uow.messages.create(
            assistant_msg
        )

        await uow.commit()