import re

from sqlalchemy.orm import Session
from core.roles import OrganizationRole
from repositories.member_repository import MemberRepository


from models.organization import Organization
from repositories.organization_repo import OrganizationRepository


class OrganizationService:
    def __init__(self, db: Session):
        self.repo = OrganizationRepository(db)
        self.member_repo = MemberRepository(db)

    def _generate_slug(self, name: str) -> str:
        """
        Convert organization name into URL-friendly slug.
        Example:
            Acme Inc -> acme-inc
            My Company Pvt Ltd -> my-company-pvt-ltd
        """
        slug = name.lower().strip()
        slug = re.sub(r"[^a-z0-9]+", "-", slug)
        slug = slug.strip("-")

        original_slug = slug
        counter = 1

        while self.repo.get_by_slug(slug):
            slug = f"{original_slug}-{counter}"
            counter += 1

        return slug

    def create_organization(
        self,
        *,
        owner_id: int,
        name: str,
        description: str | None = None,
        logo: str | None = None,
    ) -> Organization:

        slug = self._generate_slug(name)

        organization = Organization(
            name=name,
            slug=slug,
            description=description,
            logo=logo,
            owner_id=owner_id,
        )

        organization = self.repo.create(organization)
        self.member_repo.add_member(
    organization_id=organization.id,
    user_id=owner_id,
    role=OrganizationRole.OWNER,
)

        
        return organization

    def get_organization(
        self,
        organization_id: int,
    ) -> Organization | None:
        return self.repo.get_by_id(organization_id)

    def get_my_organizations(
        self,
        user_id: int,
    ) -> list[Organization]:
        return self.repo.get_user_organizations(user_id)

    def update_organization(
        self,
        organization: Organization,
    ) -> Organization:
        return self.repo.update(organization)

    def delete_organization(
        self,
        organization: Organization,
    ) -> None:
        self.repo.delete(organization)