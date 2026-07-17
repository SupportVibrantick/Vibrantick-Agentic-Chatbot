from sqlalchemy import select

from models.organization import Organization
from models.organization_member import OrganizationMember
from repositories.base import BaseRepository


class OrganizationRepository(BaseRepository[Organization]):
    """
    Repository responsible for Organization-specific queries.
    """

    model = Organization

    async def get_by_slug(
        self,
        slug: str,
    ) -> Organization | None:
        """
        Retrieve an organization by its unique slug.
        """
        stmt = (
            select(Organization)
            .where(Organization.slug == slug)
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_user_organizations(
        self,
        user_id: int,
    ) -> list[Organization]:
        """
        Return all organizations a user belongs to.
        """
        stmt = (
            select(Organization)
            .join(OrganizationMember)
            .where(
                OrganizationMember.user_id == user_id
            )
        )

        result = await self.session.execute(stmt)

        return list(result.scalars().all())