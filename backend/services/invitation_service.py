import secrets
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.roles import InvitationStatus
from models.invitation import Invitation
from models.user import User
from repositories.invitation_repository import InvitationRepository
from repositories.member_repository import MemberRepository
from repositories.organization_repository import OrganizationRepository
from repositories.user_repository import UserRepository
from schemas.invitation import (
    AcceptInvitationResponse,
    InvitationCreate,
)


class InvitationService:
    def __init__(self, db: AsyncSession):
        self.db = db

        self.repo = InvitationRepository(db)
        self.organization_repo = OrganizationRepository(db)
        self.member_repo = MemberRepository(db)
        self.user_repo = UserRepository(db)

    async def create_invitation(
        self,
        organization_id: int,
        invited_by: int,
        invitation_data: InvitationCreate,
    ) -> Invitation:

        email = invitation_data.email.strip().lower()

        organization = await self.organization_repo.get_by_id(
            organization_id
        )

        if not organization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found",
            )

        existing = await self.repo.get_pending(
            organization_id,
            email,
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Pending invitation already exists",
            )

        user = await self.user_repo.get_by_email(email)

        if user:
            if await self.member_repo.is_member(
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
            email=email,
            role=invitation_data.role,
            token=token,
            status=InvitationStatus.PENDING,
            expires_at=expires_at,
        )

        await self.repo.add(invitation)
        await self.repo.flush()
        await self.repo.refresh(invitation)
 
        return invitation

    async def list_invitations(
        self,
        organization_id: int,
    ) -> list[Invitation]:

        organization = await self.organization_repo.get_by_id(
            organization_id
        )

        if not organization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found",
            )

        return await self.repo.list_by_organization(
            organization_id
        )

    async def cancel_invitation(
        self,
        organization_id: int,
        invitation_id: int,
    ) -> Invitation:

        invitation = await self.repo.get_by_id(
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

        return await self.repo.cancel(invitation)

    async def get_invitation_by_token(
        self,
        token: str,
    ) -> Invitation:

        invitation = await self.repo.get_by_token(token)

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

    async def accept_invitation(
        self,
        token: str,
        current_user: User,
    ) -> AcceptInvitationResponse:

        invitation = await self.get_invitation_by_token(token)

        if current_user.email.lower() != invitation.email.lower():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This invitation belongs to another email address",
            )

        if await self.member_repo.is_member(
            invitation.organization_id,
            current_user.id,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already a member of this organization",
            )

        organization = await self.organization_repo.get_by_id(
            invitation.organization_id
        )

        if not organization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization no longer exists",
            )

        await self.member_repo.add_member(
            organization_id=invitation.organization_id,
            user_id=current_user.id,
            role=invitation.role,
        )

        invitation.status = InvitationStatus.ACCEPTED
        invitation.accepted_at = datetime.now(UTC)

        await self.repo.flush()
        await self.repo.refresh(invitation)
        
        return AcceptInvitationResponse(
            message="Invitation accepted successfully",
            organization_id=organization.id,
            organization_name=organization.name,
            role=invitation.role,
        )