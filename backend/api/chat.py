from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from database.unit_of_work import UnitOfWork
from dependencies.auth import get_current_user
from dependencies.database import get_uow
from models.user import User
from services.conversation_service import ConversationService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


class ChatRequest(BaseModel):
    chatbot_id: int
    message: str
    conversation_id: int | None = None


@router.post("")
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow),
):
    service = ConversationService()
    try:
        result = await service.chat(
            chatbot_id=request.chatbot_id,
            conversation_id=request.conversation_id,
            user_id=current_user.id,
            message=request.message,
            uow=uow,
        )
        return result
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.post("/stream")
async def stream_chat(
    request: ChatRequest,
    uow: UnitOfWork = Depends(get_uow),
):
    async def generate():
        service = ConversationService()
        async for token in service.stream_chat(
            chatbot_id=request.chatbot_id,
            conversation_id=request.conversation_id,
            message=request.message,
            uow=uow,
        ):
            yield token

    return StreamingResponse(
        generate(),
        media_type="text/plain",
    )