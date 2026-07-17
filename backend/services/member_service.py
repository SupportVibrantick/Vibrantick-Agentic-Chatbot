from sqlalchemy.ext.asyncio import AsyncSession
from core.roles import OrganizationRole
from models.organization_member import OrganizationMember
from repositories.member_repository import MemberRepository
from repositories.user_repository import UserRepository


class MemberService:
    def __init__(self, db: AsyncSession):
        self.member_repo = MemberRepository(db)
        self.user_repo = UserRepository(db)

    async  def add_member(
        self,
        organization_id: int,
        email: str,
        role: OrganizationRole = OrganizationRole.MEMBER,
    ) -> OrganizationMember:
        """
        Add an existing user to an organization.
        """

        # Check whether the user exists
        user = await self.user_repo.get_by_email(email)

        if not user:
            raise ValueError("User not found.")

        # Prevent duplicate memberships
        if await self.member_repo.is_member(
            organization_id=organization_id,
            user_id=user.id,
        ):
            raise ValueError("User is already a member of this organization.")

        # Create membership
        return await self.member_repo.add_member(
            organization_id=organization_id,
            user_id=user.id,
            role=role,
        )

    async def get_members(
        self,
        organization_id: int,
    ) -> list[OrganizationMember]:
        """
        Get all members of an organization.
        """
        return await self.member_repo.get_members(organization_id)

    async def update_role(
        self,
        organization_id: int,
        user_id: int,
        role: OrganizationRole,
    ) -> OrganizationMember:
        """
        Update a member's role.
        """

        member = await self.member_repo.get_member(
            organization_id=organization_id,
            user_id=user_id,
        )

        if not member:
            raise ValueError("Member not found.")

        return await self.member_repo.update_role(
            member=member,
            role=role,
        )

    async def remove_member(
        self,
        organization_id: int,
        user_id: int,
    ) -> None:
        """
        Remove a member from an organization.
        """

        member = await self.member_repo.get_member(
            organization_id=organization_id,
            user_id=user_id,
        )

        if not member:
            raise ValueError("Member not found.")

        await self.member_repo.remove_member(member)