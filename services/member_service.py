from sqlalchemy.orm import Session

from core.roles import OrganizationRole
from models.organization import OrganizationMember
from repositories.member_repository import MemberRepository
from repositories.user_repository import UserRepository


class MemberService:
    def __init__(self, db: Session):
        self.member_repo = MemberRepository(db)
        self.user_repo = UserRepository(db)

    def add_member(
        self,
        organization_id: int,
        email: str,
        role: str = OrganizationRole.MEMBER,
    ) -> OrganizationMember:
        """
        Add an existing user to an organization.
        """

        # Check whether the user exists
        user = self.user_repo.get_by_email(email)

        if not user:
            raise ValueError("User not found.")

        # Prevent duplicate memberships
        if self.member_repo.is_member(
            organization_id=organization_id,
            user_id=user.id,
        ):
            raise ValueError("User is already a member of this organization.")

        # Create membership
        return self.member_repo.add_member(
            organization_id=organization_id,
            user_id=user.id,
            role=role,
        )

    def get_members(
        self,
        organization_id: int,
    ) -> list[OrganizationMember]:
        """
        Get all members of an organization.
        """
        return self.member_repo.get_members(organization_id)

    def update_role(
        self,
        organization_id: int,
        user_id: int,
        role: str,
    ) -> OrganizationMember:
        """
        Update a member's role.
        """

        member = self.member_repo.get_member(
            organization_id=organization_id,
            user_id=user_id,
        )

        if not member:
            raise ValueError("Member not found.")

        return self.member_repo.update_role(
            member=member,
            role=role,
        )

    def remove_member(
        self,
        organization_id: int,
        user_id: int,
    ) -> None:
        """
        Remove a member from an organization.
        """

        member = self.member_repo.get_member(
            organization_id=organization_id,
            user_id=user_id,
        )

        if not member:
            raise ValueError("Member not found.")

        self.member_repo.remove_member(member)