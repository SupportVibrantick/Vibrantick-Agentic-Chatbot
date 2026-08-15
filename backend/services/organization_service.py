import re

from sqlalchemy.ext.asyncio import AsyncSession

from core.roles import OrganizationRole
from models.organization import Organization
from repositories.member_repository import MemberRepository
from repositories.organization_repository import OrganizationRepository


class OrganizationService:
    def __init__(self, db: AsyncSession):
        self.repo = OrganizationRepository(db)
        self.member_repo = MemberRepository(db)

    async def _generate_slug(
        self,
        name: str,
    ) -> str:
        """
        Convert organization name into URL-friendly slug.
        """

        slug = name.lower().strip()
        slug = re.sub(r"[^a-z0-9]+", "-", slug)
        slug = slug.strip("-")

        original_slug = slug
        counter = 1

        while await self.repo.get_by_slug(slug):
            slug = f"{original_slug}-{counter}"
            counter += 1

        return slug

    async def create_organization(
        self,
        *,
        owner_id: int,
        name: str,
        description: str | None = None,
        logo: str | None = None,
    ) -> Organization:

        slug = await self._generate_slug(name)

        organization = Organization(
            name=name,
            slug=slug,
            description=description,
            logo=logo,
            owner_id=owner_id,
        )

        await self.repo.add(organization)
        await self.repo.flush()
        await self.repo.refresh(organization)

        await self.member_repo.add_member(
            organization_id=organization.id,
            user_id=owner_id,
            role=OrganizationRole.OWNER,
        )

        return organization

    async def get_organization(
        self,
        organization_id: int,
    ) -> Organization | None:
        return await self.repo.get_by_id(
            organization_id,
        )

    async def get_my_organizations(
        self,
        user_id: int,
    ) -> list[Organization]:
        return await self.repo.get_user_organizations(
            user_id,
        )

    async def update_organization(
        self,
        organization: Organization,
    ) -> Organization:
        await self.repo.flush()
        await self.repo.refresh(organization)

        return organization

    async def delete_organization(
        self,
        organization: Organization,
    ) -> None:
        await self.repo.delete(organization)
        await self.repo.flush()