

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from models.organization import Organization, OrganizationMember


class OrganizationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
       self,
       organization: Organization,
    ) -> Organization:
         self.db.add(organization)

         await self.db.flush()
         await self.db.refresh(organization)

         return organization
    

    async def get_by_id(
        self,
        organization_id: int,
    ) -> Organization | None:
        result = await self.db.execute(
            select(Organization).where(
            Organization.id == organization_id
        )
    )

        return result.scalar_one_or_none()

    async def get_by_slug(
        self,
        slug: str,
    ) -> Organization | None:
        result = await self.db.execute(
            select(Organization).where(
                Organization.slug == slug
            )
        )
        return result.scalar_one_or_none()

    async def get_user_organizations(
        self,
        user_id: int,
        ) -> list[Organization]:
        result = await self.db.execute(
            select(Organization)
            .join(OrganizationMember)
            .where(
                OrganizationMember.user_id == user_id
            )
        )
        return list(result.scalars().all())

    async def update(
        self,
        organization: Organization,
    ) -> Organization:
        await self.db.commit()
        await self.db.refresh(organization)
        return organization 
    async def delete(
       self,
       organization: Organization,
    ) -> None:
       await self.db.delete(organization)
       await self.db.commit()