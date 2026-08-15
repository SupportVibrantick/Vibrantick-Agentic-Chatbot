from __future__ import annotations

import secrets
from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.roles import (
    InvitationStatus,
    OrganizationRole,
)
from models.invitation import Invitation
from models.organization import Organization
from models.user import User

from seeders.builders.base import  BuilderBase
class InvitationBuilder:
    """
    Builder responsible for creating Invitation entities.

    This class contains only entity creation logic and should never
    commit transactions. Transaction management is handled by the
    ExecutionManager.
    """

    DEFAULT_EXPIRY_DAYS = 7

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        organization: Organization,
        inviter: User,
        email: str,
        role: OrganizationRole = OrganizationRole.MEMBER,
        status: InvitationStatus = InvitationStatus.PENDING,
        expires_at: datetime | None = None,
    ) -> Invitation:
        """
        Create a new invitation.
        """

        invitation = Invitation(
            organization_id=organization.id,
            invited_by=inviter.id,
            email=email,
            token=secrets.token_urlsafe(32),
            role=role,
            status=status,
            expires_at=expires_at
            or (
                datetime.now(UTC)
                + timedelta(days=self.DEFAULT_EXPIRY_DAYS)
            ),
        )

        return await self.persist(invitation)
    
    async def get_or_create(
        self,
        organization: Organization,
        inviter: User,
        email: str,
        role: OrganizationRole = OrganizationRole.MEMBER,
    ) -> Invitation:
        """
        Return an existing pending invitation if one exists,
        otherwise create a new one.
        """

        stmt = select(Invitation).where(
            Invitation.organization_id == organization.id,
            Invitation.email == email,
            Invitation.status == InvitationStatus.PENDING,
        )

        result = await self.session.execute(stmt)

        invitation = result.scalar_one_or_none()

        if invitation is not None:
            return invitation

        return await self.create(
            organization=organization,
            inviter=inviter,
            email=email,
            role=role,
        )

    async def create_many(
        self,
        organization: Organization,
        inviter: User,
        emails: list[str],
        role: OrganizationRole = OrganizationRole.MEMBER,
    ) -> list[Invitation]:
        """
        Create multiple invitations.
        """

        invitations: list[Invitation] = []

        for email in emails:
            invitations.append(
                await self.get_or_create(
                    organization=organization,
                    inviter=inviter,
                    email=email,
                    role=role,
                )
            )

        return invitations