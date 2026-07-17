from sqlalchemy import select

from core.roles import InvitationStatus
from models.invitation import Invitation
from repositories.base import BaseRepository


class InvitationRepository(BaseRepository[Invitation]):
    """
    Repository responsible for Invitation-specific queries.
    """

    model = Invitation

    async def get_by_token(
        self,
        token: str,
    ) -> Invitation | None:
        stmt = (
            select(Invitation)
            .where(Invitation.token == token)
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_pending(
        self,
        organization_id: int,
        email: str,
    ) -> Invitation | None:
        stmt = (
            select(Invitation)
            .where(
                Invitation.organization_id == organization_id,
                Invitation.email == email,
                Invitation.status == InvitationStatus.PENDING,
            )
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_email(
        self,
        organization_id: int,
        email: str,
    ) -> Invitation | None:
        stmt = (
            select(Invitation)
            .where(
                Invitation.organization_id == organization_id,
                Invitation.email == email,
            )
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def list_by_organization(
        self,
        organization_id: int,
    ) -> list[Invitation]:
        stmt = (
            select(Invitation)
            .where(
                Invitation.organization_id == organization_id
            )
            .order_by(Invitation.created_at.desc())
        )

        result = await self.session.execute(stmt)

        return list(result.scalars().all())

    async def cancel(
        self,
        invitation: Invitation,
    ) -> Invitation:
        invitation.status = InvitationStatus.CANCELLED

        await self.flush()
        await self.refresh(invitation)

        return invitation