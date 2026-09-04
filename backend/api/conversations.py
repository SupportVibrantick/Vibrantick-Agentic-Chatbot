from __future__ import annotations

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from pydantic import BaseModel

from database.unit_of_work import UnitOfWork
from dependencies.auth import get_current_user
from dependencies.database import get_uow
from models.user import User


router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


class ConversationResponse(BaseModel):
    id: int
    chatbot_id: int
    title: str | None
    created_by: int | None
    created_at: object
    updated_at: object


@router.get(
    "/{conversation_id}",
    response_model=ConversationResponse,
)
async def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow),
):
    conversation = await uow.conversations.get_by_id(
        conversation_id
    )

    if conversation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found.",
        )

    chatbot = await uow.chatbots.get_by_id(
        conversation.chatbot_id
    )

    if chatbot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chatbot not found.",
        )

    member = await uow.members.get_member(
        organization_id=chatbot.organization_id,
        user_id=current_user.id,
    )

    if member is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this organization",
        )

    return conversation


@router.get(
    "/chatbot/{chatbot_id}",
    response_model=list[ConversationResponse],
)
async def list_conversations(
    chatbot_id: int,
    current_user: User = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow),
):
    chatbot = await uow.chatbots.get_by_id(chatbot_id)

    if chatbot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chatbot not found.",
        )

    member = await uow.members.get_member(
        organization_id=chatbot.organization_id,
        user_id=current_user.id,
    )

    if member is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this organization",
        )

    conversations = await uow.conversations.list_by_chatbot(
        chatbot_id
    )

    return conversations


@router.delete(
    "/{conversation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow),
):
    conversation = await uow.conversations.get_by_id(
        conversation_id
    )

    if conversation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found.",
        )

    chatbot = await uow.chatbots.get_by_id(
        conversation.chatbot_id
    )

    if chatbot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chatbot not found.",
        )

    member = await uow.members.get_member(
        organization_id=chatbot.organization_id,
        user_id=current_user.id,
    )

    if member is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this organization",
        )

    await uow.conversations.delete(conversation)
    await uow.commit()

    return None