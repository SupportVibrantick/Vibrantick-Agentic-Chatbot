from faker import Faker

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.organization import Organization
from models.user import User

from seeders.base import BaseSeeder


fake = Faker()


class OrganizationSeeder(BaseSeeder):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(
        self,
        owner: User,
        name: str | None = None,
        slug: str |None = None,
        description: str | None = None,
        logo: str | None = None,
    ) -> Organization:
        organization = Organization(
            name=name or fake.company(),
            slug=slug or fake.unique.slug(),
            description=description or fake.catch_phrase(),
            logo=logo,
            owner_id=owner.id,
        )

        await self.add(organization)
        await self.commit()
        await self.refresh(organization)

        return organization

    async def create_many(
        self,
        owner: User,
        count: int,
    ) -> list[Organization]:
        organizations = []

        for _ in range(count):
            organization = Organization(
                name=fake.company(),
                slug=fake.unique.slug(),
                description=fake.catch_phrase(),
                owner_id=owner.id,
            )

            self.session.add(organization)
            organizations.append(organization)

        await self.commit()

        for organization in organizations:
            await self.refresh(organization)

        return organizations

    async def get_or_create(
        self,
        owner: User,
        slug: str,
        name: str | None = None,
        description: str | None = None,
        logo: str | None = None,
    ) -> Organization:
        stmt = select(Organization).where(
            Organization.slug == slug
        )

        result = await self.session.execute(stmt)
        organization = result.scalar_one_or_none()

        if organization:
            return organization

        return await self.create(
            owner=owner,
            name=name,
            slug=slug,
            description=description,
            logo=logo,
        )