import secrets
from datetime import datetime, timedelta, UTC

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from core.roles import InvitationStatus

from models.invitation import Invitation

from repositories.invitation_repository import InvitationRepository
from repositories.organization_repo import OrganizationRepository
from repositories.member_repository import MemberRepository
from repositories.user_repository import UserRepository

from schemas.invitation import InvitationCreate


class InvitationService:

    def __init__(self, db: Session):
        self.db = db

        self.repo = InvitationRepository(db)
        self.organization_repo = OrganizationRepository(db)
        self.member_repo = MemberRepository(db)
        self.user_repo = UserRepository(db)

    def create_invitation(
        self,
        organization_id: int,
        invited_by: int,
        invitation_data: InvitationCreate,
    ):

        organization = self.organization_repo.get_by_id(
            organization_id
        )

        if not organization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found",
            )

        existing = self.repo.get_pending(
            organization_id,
            invitation_data.email,
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Pending invitation already exists",
            )

        user = self.user_repo.get_by_email(
            invitation_data.email
        )

        if user:
            if self.member_repo.is_member(
                organization_id,
                user.id,
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User is already a member of this organization",
                )

        token = secrets.token_urlsafe(32)

        expires_at = datetime.now(UTC) + timedelta(days=7)

        invitation = Invitation(
            organization_id=organization_id,
            invited_by=invited_by,
            email=invitation_data.email,
            role=invitation_data.role,
            token=token,
            status=InvitationStatus.PENDING,
            expires_at=expires_at,
        )

        return self.repo.create(invitation)

    def list_invitations(
        self,
        organization_id: int,
    ):
        organization = self.organization_repo.get_by_id(
            organization_id
        )

        if not organization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found",
            )

        return self.repo.list_by_organization(
            organization_id
        )

    def cancel_invitation(
        self,
        organization_id: int,
        invitation_id: int,
        ):
        invitation = self.repo.get_by_id(
            invitation_id
            )
        if not invitation:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation not found",
        )

        if invitation.organization_id != organization_id:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation not found",
        )

        if invitation.status != InvitationStatus.PENDING:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only pending invitations can be cancelled",
        )
        
        
        return self.repo.cancel(invitation)