from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import get_db
from dependencies.auth import get_current_user

from models.user import User

from schemas.invitation import (
    InvitationDetailsResponse,
    AcceptInvitationResponse,
)

from services.invitation_service import InvitationService


router = APIRouter(
    prefix="/invitations",
    tags=["Public Invitations"],
)


@router.get(
    "/{token}",
    response_model=InvitationDetailsResponse,
)
async def get_invitation(
    token: str,
    db: AsyncSession = Depends(get_db),
):
    service = InvitationService(db)

    invitation = await service.get_invitation_by_token(
        token,
    )

    return InvitationDetailsResponse(
        organization_name=invitation.organization.name,
        email=invitation.email,
        role=invitation.role,
        expires_at=invitation.expires_at,
        status=invitation.status,
    )


@router.post(
    "/{token}/accept",
    response_model=AcceptInvitationResponse,
)
async def accept_invitation(
    token: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = InvitationService(db)

    return await service.accept_invitation(
        token=token,
        current_user=current_user,
    )