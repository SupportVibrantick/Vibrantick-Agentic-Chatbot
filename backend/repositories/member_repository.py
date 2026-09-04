
from __future__ import annotations

from sqlalchemy import select

from core.roles import OrganizationRole
from models.organization_member import OrganizationMember
from repositories.base_repository import BaseRepository


class MemberRepository(BaseRepository[OrganizationMember]):
    """
    Repository responsible for OrganizationMember-specific queries.
    """

    model = OrganizationMember

    async def add_member(
        self,
        organization_id: int,
        user_id: int,
        role: OrganizationRole,
    ) -> OrganizationMember:
        member = OrganizationMember(
            organization_id=organization_id,
            user_id=user_id,
            role=role,
        )

        await self.add(member)
        await self.flush()
        await self.refresh(member)

        return member

    async def get_member(
        self,
        organization_id: int,
        user_id: int,
    ) -> OrganizationMember | None:
        stmt = (
            select(OrganizationMember)
            .where(
                OrganizationMember.organization_id == organization_id,
                OrganizationMember.user_id == user_id,
            )
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_members(
        self,
        organization_id: int,
    ) -> list[OrganizationMember]:
        stmt = (
            select(OrganizationMember)
            .where(
                OrganizationMember.organization_id == organization_id
            )
        )

        result = await self.session.execute(stmt)

        return list(result.scalars().all())

    async def is_member(
        self,
        organization_id: int,
        user_id: int,
    ) -> bool:
        return (
            await self.get_member(
                organization_id,
                user_id,
            )
        ) is not None

    async def update_role(
        self,
        member: OrganizationMember,
        role: OrganizationRole,
    ) -> OrganizationMember:
        member.role = role

        await self.flush()
        await self.refresh(member)

        return member

    async def remove_member(
        self,
        member: OrganizationMember,
    ) -> None:
        await self.delete(member)