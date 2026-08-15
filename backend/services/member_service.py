from sqlalchemy.ext.asyncio import AsyncSession

from core.roles import OrganizationRole
from models.organization_member import OrganizationMember
from models.user import User
from repositories.member_repository import MemberRepository
from repositories.organization_repository import OrganizationRepository
from repositories.user_repository import UserRepository


class MemberService:
    def __init__(self, db: AsyncSession):
        self.member_repo = MemberRepository(db)
        self.user_repo = UserRepository(db)
        self.organization_repo = OrganizationRepository(db)

    async def add_member(
        self,
        current_user: User,
        organization_id: int,
        email: str,
        role: OrganizationRole = OrganizationRole.MEMBER,
    ) -> OrganizationMember:
        """
        Add an existing user to an organization.
        """

        # Verify organization exists
        organization = await self.organization_repo.get_by_id(
            organization_id,
        )

        if organization is None:
            raise ValueError("Organization not found.")

        # Verify current user is a member
        current_membership = await self.member_repo.get_member(
            organization_id=organization_id,
            user_id=current_user.id,
        )

        if current_membership is None:
            raise ValueError(
                "You are not a member of this organization."
            )

        # Verify permissions
        if current_membership.role not in (
            OrganizationRole.OWNER,
            OrganizationRole.ADMIN,
        ):
            raise ValueError(
                "Administrator permission required."
            )

        # Check whether the invited user exists
        user = await self.user_repo.get_by_email(email)

        if user is None:
            raise ValueError("User not found.")

        # Prevent duplicate memberships
        if await self.member_repo.is_member(
            organization_id=organization_id,
            user_id=user.id,
        ):
            raise ValueError(
                "User is already a member of this organization."
            )

        return await self.member_repo.add_member(
            organization_id=organization_id,
            user_id=user.id,
            role=role,
        )

    async def get_members(
        self,
        current_user: User,
        organization_id: int,
    ) -> list[OrganizationMember]:
        """
        Get all members of an organization.
        """

        organization = await self.organization_repo.get_by_id(
            organization_id,
        )

        if organization is None:
            raise ValueError("Organization not found.")

        membership = await self.member_repo.get_member(
            organization_id=organization_id,
            user_id=current_user.id,
        )

        if membership is None:
            raise ValueError(
                "You are not a member of this organization."
            )

        return await self.member_repo.get_members(
            organization_id,
        )

    async def update_role(
        self,
        current_user: User,
        organization_id: int,
        user_id: int,
        role: OrganizationRole,
    ) -> OrganizationMember:
        """
        Update a member's role.
        """

        organization = await self.organization_repo.get_by_id(
            organization_id,
        )

        if organization is None:
            raise ValueError("Organization not found.")

        current_membership = await self.member_repo.get_member(
            organization_id=organization_id,
            user_id=current_user.id,
        )

        if current_membership is None:
            raise ValueError(
                "You are not a member of this organization."
            )

        if current_membership.role not in (
            OrganizationRole.ADMIN,
            OrganizationRole.OWNER,
        ):
            raise ValueError(
                "Administrator permission required."
            )

        member = await self.member_repo.get_member(
            organization_id=organization_id,
            user_id=user_id,
        )

        if member is None:
            raise ValueError("Member not found.")

        if member.role == OrganizationRole.OWNER:
            raise ValueError(
                "The organization owner cannot be modified."
            )

        if role == OrganizationRole.OWNER:
            raise ValueError(
                "Ownership cannot be assigned through this endpoint."
            )

        return await self.member_repo.update_role(
            member=member,
            role=role,
        )

    async def remove_member(
        self,
        current_user: User,
        organization_id: int,
        user_id: int,
    ) -> None:
        """
        Remove a member from an organization.
        """

        organization = await self.organization_repo.get_by_id(
            organization_id,
        )

        if organization is None:
            raise ValueError("Organization not found.")

        current_membership = await self.member_repo.get_member(
            organization_id=organization_id,
            user_id=current_user.id,
        )

        if current_membership is None:
            raise ValueError(
                "You are not a member of this organization."
            )

        if current_membership.role not in (
            OrganizationRole.ADMIN,
            OrganizationRole.OWNER,
        ):
            raise ValueError(
                "Administrator permission required."
            )

        member = await self.member_repo.get_member(
            organization_id=organization_id,
            user_id=user_id,
        )

        if member is None:
            raise ValueError("Member not found.")

        if member.role == OrganizationRole.OWNER:
            raise ValueError(
                "The organization owner cannot be removed."
            )

        await self.member_repo.remove_member(
            member,
        )