from fastapi import APIRouter, Depends, HTTPException, status

from database.unit_of_work import UnitOfWork
from dependencies.auth import get_current_user
from dependencies.database import get_uow
from dependencies.organization import (
    require_admin,
    require_member,
)
from models.user import User
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
    current_user: User = Depends(get_current_user),
    _organization=Depends(require_admin),
    uow: UnitOfWork = Depends(get_uow),
):
    service = ChatbotService(uow)

    chatbot = await service.create_chatbot(
        organization_id=organization_id,
        created_by=current_user.id,
        **chatbot_data.model_dump(),
    )

    return chatbot


@router.get(
    "/organizations/{organization_id}",
    response_model=ChatbotListResponse,
)
async def list_chatbots(
    organization_id: int,
    _organization=Depends(require_member),
    uow: UnitOfWork = Depends(get_uow),
):
    service = ChatbotService(uow)

    chatbots = await service.list_chatbots(
        organization_id,
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
    current_user: User = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow),
):
    service = ChatbotService(uow)

    chatbot = await service.get_chatbot(
        chatbot_id,
    )

    if chatbot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chatbot not found.",
        )

    membership = await uow.members.get_member(
        organization_id=chatbot.organization_id,
        user_id=current_user.id,
    )

    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this organization",
        )

    return chatbot
