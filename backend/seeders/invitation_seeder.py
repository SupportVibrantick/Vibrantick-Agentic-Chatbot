from datetime import UTC, datetime, timedelta
import secrets

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.roles import (
    InvitationStatus,
    OrganizationRole,
)

from models.invitation import Invitation
from models.organization import Organization
from models.user import User

from seeders.base import BaseSeeder


class InvitationSeeder(BaseSeeder):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(
        self,
        organization: Organization,
        inviter: User,
        email: str,
        role: OrganizationRole = OrganizationRole.MEMBER,
        status: InvitationStatus = InvitationStatus.PENDING,
        expires_at: datetime | None = None,
    ) -> Invitation:

        invitation = Invitation(
            organization_id=organization.id,
            invited_by=inviter.id,
            email=email,
            token=secrets.token_urlsafe(32),
            role=role,
            status=status,
            expires_at=expires_at
            or (datetime.now(UTC) + timedelta(days=7)),
        )

        await self.add(invitation)
        await self.commit()
        await self.refresh(invitation)

        return invitation

    async def create_many(
        self,
        organization: Organization,
        inviter: User,
        emails: list[str],
        role: OrganizationRole = OrganizationRole.MEMBER,
    ) -> list[Invitation]:

        invitations: list[Invitation] = []

        for email in emails:
            invitation = await self.get_or_create(
                organization=organization,
                inviter=inviter,
                email=email,
                role=role,
            )
            invitations.append(invitation)

        return invitations

    async def get_or_create(
        self,
        organization: Organization,
        inviter: User,
        email: str,
        role: OrganizationRole = OrganizationRole.MEMBER,
    ) -> Invitation:

        stmt = select(Invitation).where(
            Invitation.organization_id == organization.id,
            Invitation.email == email,
            Invitation.status == InvitationStatus.PENDING,
        )

        result = await self.session.execute(stmt)
        invitation = result.scalar_one_or_none()

        if invitation:
            return invitation

        return await self.create(
            organization=organization,
            inviter=inviter,
            email=email,
            role=role,
        )