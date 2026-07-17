from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import get_db
from dependencies.auth import get_current_user
from models.user import User
from schemas.member import (
    MemberCreate,
    MemberResponse,
    MemberUpdateRole,
)
from services.member_service import MemberService

router = APIRouter(
    prefix="/organizations",
    tags=["Members"],
)

@router.post(
    "/{organization_id}/members",
    response_model=MemberResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_member(
    organization_id: int,
    data: MemberCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = MemberService(db)

    try:
        return await service.add_member(
            organization_id=organization_id,
            email=data.email,
            role=data.role,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
        
@router.get(
    "/{organization_id}/members",
    response_model=list[MemberResponse],
)
async def get_members(
    organization_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = MemberService(db)

    return await service.get_members(
        organization_id,
    )

@router.patch(
    "/{organization_id}/members/{user_id}",
    response_model=MemberResponse,
)
async  def update_role(
    organization_id: int,
    user_id: int,
    data: MemberUpdateRole,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = MemberService(db)

    try:
        return await service.update_role(
            organization_id=organization_id,
            user_id=user_id,
            role=data.role,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
        
@router.delete(
    "/{organization_id}/members/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_member(
    organization_id: int,
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = MemberService(db)

    try:
        await service.remove_member(
            organization_id=organization_id,
            user_id=user_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )