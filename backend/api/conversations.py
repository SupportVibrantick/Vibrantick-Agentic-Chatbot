from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from database.unit_of_work import UnitOfWork
from schemas.conversation import (
    ChatRequest,
    ChatResponse,
)
from services.conversation_service import ConversationService

router = APIRouter(
    prefix="/chatbots/{chatbot_id}/chat",
    tags=["Conversations"],
)

service = ConversationService()


@router.post(
    "",
    response_model=ChatResponse,
)
async def chat(
    chatbot_id: int,
    request: ChatRequest,
):
    async with UnitOfWork() as uow:
        try:
            response = await service.chat(
                chatbot_id=chatbot_id,
                message=request.message,
                uow=uow,
            )

            return ChatResponse(
                response=response,
            )

        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc