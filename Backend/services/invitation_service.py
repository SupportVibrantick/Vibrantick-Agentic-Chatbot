import secrets
from datetime import datetime, timedelta, UTC

from models.invitation import Invitation

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from core.roles import InvitationStatus
from models.user import User



from repositories.invitation_repository import InvitationRepository
from repositories.organization_repo import OrganizationRepository
from repositories.member_repository import MemberRepository
from repositories.user_repository import UserRepository



from schemas.invitation import (
    InvitationCreate,
    AcceptInvitationResponse,
)



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
        email = invitation_data.email.strip().lower()

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
            email,
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Pending invitation already exists",
            )

        user = self.user_repo.get_by_email(
            email
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
            email = email,
            role=invitation_data.role,
            token=token,
            status=InvitationStatus.PENDING,
            expires_at=expires_at,
        )

        invitation = self.repo.create(invitation)
        
        return invitation

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
    
    
    def get_invitation_by_token(
        self,
        token: str,
   ):
        invitation = self.repo.get_by_token(token)

        if not invitation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invitation not found",
                )

        if invitation.status != InvitationStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invitation is no longer valid",
                )

        if invitation.expires_at < datetime.now(UTC):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invitation has expired",
                )
        return invitation
    
    def accept_invitation(
        self,
        token: str,
        current_user: User,
    ):
        invitation = self.get_invitation_by_token(token)

        if current_user.email.lower() != invitation.email.lower():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This invitation belongs to another email address",
            )

        if self.member_repo.is_member(
            invitation.organization_id,
            current_user.id,
        ):
            
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already a member of this organization",
                )
        organization = self.organization_repo.get_by_id(
            invitation.organization_id
        )

        if not organization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization no longer exists",
        )

        self.member_repo.add_member(
            organization_id=invitation.organization_id,
            user_id=current_user.id,
            role=invitation.role,
        )

        invitation.status = InvitationStatus.ACCEPTED
        invitation.accepted_at = datetime.now(UTC)
        
        self.repo.update(invitation)
        
        return AcceptInvitationResponse(
            message="Invitation accepted successfully",
            organization_id=organization.id,
            organization_name=organization.name,
            role=invitation.role,
            )