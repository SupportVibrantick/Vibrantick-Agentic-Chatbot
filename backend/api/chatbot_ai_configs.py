from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from database.unit_of_work import UnitOfWork
from schemas.chatbot_ai_config import (
    ChatbotAIConfigCreate,
    ChatbotAIConfigResponse,
    ChatbotAIConfigUpdate,
)
from services.chatbot_ai_config_service import ChatbotAIConfigService

router = APIRouter(
    prefix="/chatbots/{chatbot_id}/ai-config",
    tags=["Chatbot AI Config"],
)

service = ChatbotAIConfigService()


@router.post(
    "",
    response_model=ChatbotAIConfigResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_ai_config(
    chatbot_id: int,
    data: ChatbotAIConfigCreate,
):
    async with UnitOfWork() as uow:
        try:
            return await service.create_config(
                chatbot_id=chatbot_id,
                data=data,
                uow=uow,
            )
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc),
            ) from exc


@router.get(
    "",
    response_model=ChatbotAIConfigResponse,
)
async def get_ai_config(
    chatbot_id: int,
):
    async with UnitOfWork() as uow:
        config = await service.get_config(
            chatbot_id=chatbot_id,
            uow=uow,
        )

        if config is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="AI configuration not found.",
            )

        return config


@router.patch(
    "",
    response_model=ChatbotAIConfigResponse,
)
async def update_ai_config(
    chatbot_id: int,
    data: ChatbotAIConfigUpdate,
):
    async with UnitOfWork() as uow:
        try:
            return await service.update_config(
                chatbot_id=chatbot_id,
                data=data,
                uow=uow,
            )
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc


@router.delete(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_ai_config(
    chatbot_id: int,
):
    async with UnitOfWork() as uow:
        try:
            await service.delete_config(
                chatbot_id=chatbot_id,
                uow=uow,
            )
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc