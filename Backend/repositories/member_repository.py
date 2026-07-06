from unittest import result

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.roles import OrganizationRole
from models.organization import OrganizationMember


class MemberRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def add_member(
        self,
        organization_id: int,
        user_id: int,
        role: OrganizationRole,
    ) -> OrganizationMember:

   
        """
        Create a new organization membership.
        """
        member = OrganizationMember(
            organization_id=organization_id,
            user_id=user_id,
            role=role,
        )

        await self.db.add(member)
        await self.db.commit()
        await self.db.refresh(member)

        return member

    async def get_member(
        self,
        organization_id: int,
        user_id: int,
    ) -> OrganizationMember | None:
        result = await self.db.execute(
            select(OrganizationMember).where(
                OrganizationMember.organization_id == organization_id,
                OrganizationMember.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_members(
        self,
        organization_id: int,
    ) -> list[OrganizationMember]:
        result = await self.db.execute(
            select(OrganizationMember).where(
                OrganizationMember.organization_id == organization_id
            )
        )
        return list(result.scalars().all())

    async def is_member(
        self,
        organization_id: int,
        user_id: int,
    ) -> bool:
        result = await self.db.execute(
            select(OrganizationMember).where(
                OrganizationMember.organization_id == organization_id,
                OrganizationMember.user_id == user_id,
            )
      )
        return result.scalar_one_or_none() is not None

    async def update_role(
        self,
        member: OrganizationMember,
        role: OrganizationRole,
    ) -> OrganizationMember:
        member.role = role
        await self.db.commit()
        await self.db.refresh(member)
        return member

    async def remove_member(
        self,
        member: OrganizationMember,
    ) -> None:
        """
        Remove a member from an organization.
        """
        await self.db.delete(member)
        await self.db.commit()