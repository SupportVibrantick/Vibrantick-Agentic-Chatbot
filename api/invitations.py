from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database.session import get_db

from dependencies.auth import get_current_user
from dependencies.organization import require_admin

from models.user import User
from models.organization import Organization

from schemas.invitation import (
    InvitationCreate,
    InvitationResponse,
    InvitationListResponse,
)

from services.invitation_service import InvitationService


router = APIRouter(
    prefix="/organizations/{organization_id}/invitations",
    tags=["Invitations"],
)


@router.post(
    "",
    response_model=InvitationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_invitation(
    data: InvitationCreate,
    organization: Organization = Depends(require_admin),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = InvitationService(db)

    return service.create_invitation(
        organization_id=organization.id,
        invited_by=current_user.id,
        invitation_data=data,
    )


@router.get(
    "",
    response_model=InvitationListResponse,
)
def list_invitations(
    organization: Organization = Depends(require_admin),
    db: Session = Depends(get_db),
):
    service = InvitationService(db)

    invitations = service.list_invitations(
        organization.id,
    )

    return InvitationListResponse(
        invitations=invitations,
    )


@router.delete(
    "/{invitation_id}",
    response_model=InvitationResponse,
)
def cancel_invitation(
    invitation_id: int,
    organization: Organization = Depends(require_admin),
    db: Session = Depends(get_db),
):
    service = InvitationService(db)

    return service.cancel_invitation(
        organization_id=organization.id,
        invitation_id=invitation_id,
    )