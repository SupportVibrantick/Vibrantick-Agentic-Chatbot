from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)

from database.unit_of_work import UnitOfWork
from dependencies.database import get_uow
from schemas.knowledge_source import KnowledgeSourceResponse
from services.knowledge_source_service import (
    KnowledgeSourceService,
)


router = APIRouter(
    prefix="/knowledge-bases",
    tags=["Knowledge Sources"],
)


@router.post(
    "/{knowledge_base_id}/sources/upload",
    response_model=KnowledgeSourceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_source(
    knowledge_base_id: int,
    file: UploadFile = File(...),
    uow: UnitOfWork = Depends(get_uow),
):
    content = await file.read()

    service = KnowledgeSourceService(uow)

    try:
        source = await service.upload_file(
            knowledge_base_id=knowledge_base_id,
            filename=file.filename or "uploaded_file",
            content=content,
            content_type=file.content_type or "",
        )

        return source

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc