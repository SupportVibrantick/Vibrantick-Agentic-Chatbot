from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.roles import OrganizationRole

from models.organization import Organization
from models.organization_member import OrganizationMember
from models.user import User

from seeders.base import BaseSeeder


class MemberSeeder(BaseSeeder):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(
        self,
        organization: Organization,
        user: User,
        role: OrganizationRole = OrganizationRole.MEMBER,
    ) -> OrganizationMember:

        member = OrganizationMember(
            organization_id=organization.id,
            user_id=user.id,
            role=role,
        )

        await self.add(member)
        await self.commit()
        await self.refresh(member)

        return member

    async def create_many(
        self,
        organization: Organization,
        users: list[User],
        role: OrganizationRole = OrganizationRole.MEMBER,
    ) -> list[OrganizationMember]:

        members: list[OrganizationMember] = []

        for user in users:
            member = await self.get_or_create(
                organization=organization,
                user=user,
                role=role,
            )
            members.append(member)

        return members

    async def get_or_create(
        self,
        organization: Organization,
        user: User,
        role: OrganizationRole = OrganizationRole.MEMBER,
    ) -> OrganizationMember:

        stmt = select(OrganizationMember).where(
            OrganizationMember.organization_id == organization.id,
            OrganizationMember.user_id == user.id,
        )

        result = await self.session.execute(stmt)
        member = result.scalar_one_or_none()

        if member:
            return member

        return await self.create(
            organization=organization,
            user=user,
            role=role,
        )

    async def owner(
        self,
        organization: Organization,
        user: User,
    ) -> OrganizationMember:

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

        return await self.get_or_create(
            organization=organization,
            user=user,
            role=OrganizationRole.MEMBER,
        )