from __future__ import annotations

from database.unit_of_work import UnitOfWork

from services.documents.retriever import (
    DocumentRetriever,
)

from services.llm.provider_factory import (
    ProviderFactory,
)

from services.llm.types import (
    LLMMessage,
    LLMRequest,
    MessageRole,
)


class RAGService:
    """
    Retrieval-Augmented Generation service.

    Pipeline

    User Question
          │
          ▼
    Retrieve Context
          │
          ▼
    DeepSeek
          │
          ▼
    Final Answer
    """

    def __init__(
        self,
        uow: UnitOfWork,
    ):
        self.uow = uow

        self.retriever = DocumentRetriever(
            uow,
        )

        self.llm = ProviderFactory.create()

    async def ask(
        self,
        question: str,
    ) -> str:

        context = (
            await self.retriever.retrieve_context(
                question,
            )
        )

        system_prompt = f"""
You are an AI assistant.

Answer ONLY using the provided context.

If the answer is not contained in the context,
reply:

"I don't know based on the uploaded documents."

Context:

{context}
"""

        request = LLMRequest(
            messages=[
                LLMMessage(
                    role=MessageRole.SYSTEM,
                    content=system_prompt,
                ),
                LLMMessage(
                    role=MessageRole.USER,
                    content=question,
                ),
            ],
        )

        return await self.llm.chat(
            request,
        )