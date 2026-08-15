from fastapi import APIRouter, Depends, HTTPException, status

from database.unit_of_work import UnitOfWork
from dependencies.database import get_uow
from dependencies.organization import (
    require_chatbot_admin,
    require_chatbot_member,
    require_knowledge_base_admin,
    require_knowledge_base_member,
)
from schemas.knowledge_base import (
    KnowledgeBaseCreate,
    KnowledgeBaseListResponse,
    KnowledgeBaseResponse,
    KnowledgeBaseUpdate,
)
from services.knowledge_base_service import (
    KnowledgeBaseService,
)


router = APIRouter(
    prefix="/knowledge-bases",
    tags=["Knowledge Bases"],
)


@router.post(
    "/chatbots/{chatbot_id}",
    response_model=KnowledgeBaseResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_knowledge_base(
    chatbot_id: int,
    data: KnowledgeBaseCreate,
    _chatbot=Depends(require_chatbot_admin),
    uow: UnitOfWork = Depends(get_uow),
):
    service = KnowledgeBaseService()

    try:
        return await service.create(
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
    "/chatbots/{chatbot_id}",
    response_model=KnowledgeBaseListResponse,
)
async def list_knowledge_bases(
    chatbot_id: int,
    _chatbot=Depends(require_chatbot_member),
    uow: UnitOfWork = Depends(get_uow),
):
    service = KnowledgeBaseService()

    items = await service.list_by_chatbot(
        chatbot_id,
        uow,
    )

    return KnowledgeBaseListResponse(
        items=items,
        total=len(items),
    )


@router.get(
    "/{knowledge_base_id}",
    response_model=KnowledgeBaseResponse,
)
async def get_knowledge_base(
    knowledge_base_id: int,
    _knowledge_base=Depends(
        require_knowledge_base_member
    ),
    uow: UnitOfWork = Depends(get_uow),
):
    service = KnowledgeBaseService()

    knowledge_base = await service.get_by_id(
        knowledge_base_id,
        uow,
    )

    if knowledge_base is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge Base not found.",
        )

    return knowledge_base


@router.patch(
    "/{knowledge_base_id}",
    response_model=KnowledgeBaseResponse,
)
async def update_knowledge_base(
    knowledge_base_id: int,
    data: KnowledgeBaseUpdate,
    _knowledge_base=Depends(
        require_knowledge_base_admin
    ),
    uow: UnitOfWork = Depends(get_uow),
):
    service = KnowledgeBaseService()

    knowledge_base = await service.get_by_id(
        knowledge_base_id,
        uow,
    )

    if knowledge_base is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge Base not found.",
        )

    try:
        return await service.update(
            knowledge_base,
            data,
            uow,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{knowledge_base_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_knowledge_base(
    knowledge_base_id: int,
    _knowledge_base=Depends(
        require_knowledge_base_admin
    ),
    uow: UnitOfWork = Depends(get_uow),
):
    service = KnowledgeBaseService()

    knowledge_base = await service.get_by_id(
        knowledge_base_id,
        uow,
    )

    if knowledge_base is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge Base not found.",
        )

    await service.delete(
        knowledge_base,
        uow,
    )