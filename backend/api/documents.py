from __future__ import annotations

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)

from database.unit_of_work import UnitOfWork
from dependencies.auth import get_current_user
from dependencies.database import get_uow
from models.user import User
from schemas.document import (
    DocumentListResponse,
    DocumentResponse,
)
from services.documents.document_service import (
    DocumentService,
)

router = APIRouter(
    prefix="/knowledge-bases/{knowledge_base_id}/documents",
    tags=["Documents"],
)


@router.post(
    "",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    knowledge_base_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow),
):
    service = DocumentService(uow)
    try:
        return await service.upload_document(
            knowledge_base_id=knowledge_base_id,
            file=file,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get(
    "",
    response_model=DocumentListResponse,
)
async def list_documents(
    knowledge_base_id: int,
    current_user: User = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow),
):
    service = DocumentService(uow)
    try:
        documents = await service.list_documents(
            knowledge_base_id,
        )
        return DocumentListResponse(
            items=documents,
            total=len(documents),
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )