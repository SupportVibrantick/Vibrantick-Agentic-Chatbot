from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.organization import Organization
from models.user import User


class OrganizationBuilder:
    """
    Builder responsible for creating Organization entities.

    This class contains only entity creation logic and should never
    commit transactions. Transaction management is handled by the
    ExecutionManager.
    """

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        owner: User,
        name: str,
        slug: str,
        description: str | None = None,
    ) -> Organization:
        """
        Create a new organization.
        """

        organization = Organization(
            owner=owner,
            name=name,
            slug=slug,
            description=description,
        )

        self.session.add(organization)

        await self.session.flush()
        await self.session.refresh(organization)

        return organization

    async def get_or_create(
        self,
        owner: User,
        name: str,
        slug: str,
        description: str | None = None,
    ) -> Organization:
        """
        Return an existing organization if one exists with the given slug,
        otherwise create a new one.
        """

        stmt = select(Organization).where(
            Organization.slug == slug
        )

        result = await self.session.execute(stmt)

        organization = result.scalar_one_or_none()

        if organization is not None:
            return organization

        return await self.create(
            owner=owner,
            name=name,
            slug=slug,
            description=description,
        )