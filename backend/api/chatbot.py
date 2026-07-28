from fastapi import APIRouter, HTTPException, status

from database.unit_of_work import UnitOfWork
from schemas.chatbot import (
    ChatbotCreate,
    ChatbotListResponse,
    ChatbotResponse,
)
from services.chatbot_service import ChatbotService

router = APIRouter(
    prefix="/chatbots",
    tags=["Chatbots"],
)


@router.post(
    "/organizations/{organization_id}",
    response_model=ChatbotResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_chatbot(
    organization_id: int,
    chatbot_data: ChatbotCreate,
):
    async with UnitOfWork() as uow:

        service = ChatbotService(uow)

        chatbot = await service.create_chatbot(
            organization_id=organization_id,
            created_by=1,  # temporary
            **chatbot_data.model_dump(),
        )

        return chatbot


@router.get(
    "/organizations/{organization_id}",
    response_model=ChatbotListResponse,
)
async def list_chatbots(
    organization_id: int,
):
    async with UnitOfWork() as uow:

        service = ChatbotService(uow)

        chatbots = await service.list_chatbots(
            organization_id
        )

        return ChatbotListResponse(
            items=chatbots,
            total=len(chatbots),
        )


@router.get(
    "/{chatbot_id}",
    response_model=ChatbotResponse,
)
async def get_chatbot(
    chatbot_id: int,
):
    async with UnitOfWork() as uow:

        service = ChatbotService(uow)

        chatbot = await service.get_chatbot(
            chatbot_id
        )

        if chatbot is None:
            raise HTTPException(
                status_code=404,
                detail="Chatbot not found.",
            )

        return chatbot