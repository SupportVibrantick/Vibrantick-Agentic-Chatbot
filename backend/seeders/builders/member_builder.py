from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.roles import OrganizationRole
from models.organization import Organization
from models.organization_member import OrganizationMember
from models.user import User


class MemberBuilder:
    """
    Builder responsible for creating OrganizationMember entities.

    This class contains only entity creation logic and should never
    commit transactions. Transaction management is handled by the
    ExecutionManager.
    """

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        organization: Organization,
        user: User,
        role: OrganizationRole = OrganizationRole.MEMBER,
    ) -> OrganizationMember:
        """
        Create a new organization member.
        """

        member = OrganizationMember(
            organization_id=organization.id,
            user_id=user.id,
            role=role,
        )

        self.session.add(member)

        await self.session.flush()
        await self.session.refresh(member)

        return member

    async def get_or_create(
        self,
        organization: Organization,
        user: User,
        role: OrganizationRole = OrganizationRole.MEMBER,
    ) -> OrganizationMember:
        """
        Return an existing organization member if one exists,
        otherwise create a new one.
        """

        stmt = select(OrganizationMember).where(
            OrganizationMember.organization_id == organization.id,
            OrganizationMember.user_id == user.id,
        )

        result = await self.session.execute(stmt)

        member = result.scalar_one_or_none()

        if member is not None:
            return member

        return await self.create(
            organization=organization,
            user=user,
            role=role,
        )

    async def create_many(
        self,
        organization: Organization,
        users: list[User],
        role: OrganizationRole = OrganizationRole.MEMBER,
    ) -> list[OrganizationMember]:
        """
        Create multiple organization members.
        """

        members: list[OrganizationMember] = []

        for user in users:
            members.append(
                await self.get_or_create(
                    organization=organization,
                    user=user,
                    role=role,
                )
            )

        return members

    async def owner(
        self,
        organization: Organization,
        user: User,
    ) -> OrganizationMember:
        """
        Create or retrieve the organization owner.
        """

        return await self.get_or_create(
            organization=organization,
            user=user,
            role=OrganizationRole.OWNER,
        )

    async def admin(
        self,
        organization: Organization,
        user: User,
    ) -> OrganizationMember:
        """
        Create or retrieve the organization administrator.
        """

        return await self.get_or_create(
            organization=organization,
            user=user,
            role=OrganizationRole.ADMIN,
        )

    async def member(
        self,
        organization: Organization,
        user: User,
    ) -> OrganizationMember:
        """
        Create or retrieve a regular organization member.
        """

        return await self.get_or_create(
            organization=organization,
            user=user,
            role=OrganizationRole.MEMBER,
        )