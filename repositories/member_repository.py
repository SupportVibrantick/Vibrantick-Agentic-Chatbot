from sqlalchemy.orm import Session

from core.roles import OrganizationRole
from models.organization import OrganizationMember


class MemberRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def add_member(
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

        self.db.add(member)
        self.db.commit()
        self.db.refresh(member)

        return member

    def get_member(
        self,
        organization_id: int,
        user_id: int,
    ) -> OrganizationMember | None:
        """
        Get a specific member of an organization.
        """
        return (
            self.db.query(OrganizationMember)
            .filter(
                OrganizationMember.organization_id == organization_id,
                OrganizationMember.user_id == user_id,
            )
            .first()
        )

    def get_members(
        self,
        organization_id: int,
    ) -> list[OrganizationMember]:
        """
        Get all members of an organization.
        """
        return (
            self.db.query(OrganizationMember)
            .filter(
                OrganizationMember.organization_id == organization_id
            )
            .all()
        )

    def is_member(
        self,
        organization_id: int,
        user_id: int,
    ) -> bool:
        """
        Check whether a user belongs to an organization.
        """
        member = (
            self.db.query(OrganizationMember)
            .filter(
                OrganizationMember.organization_id == organization_id,
                OrganizationMember.user_id == user_id,
            )
            .first()
        )

        return member is not None

    def update_role(
        self,
        member: OrganizationMember,
        role: OrganizationRole,
    ) -> OrganizationMember:
        """
        Update a member's role.
        """
        member.role = role

        self.db.commit()
        self.db.refresh(member)

        return member

    def remove_member(
        self,
        member: OrganizationMember,
    ) -> None:
        """
        Remove a member from an organization.
        """
        self.db.delete(member)
        self.db.commit()