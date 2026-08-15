from __future__ import annotations

from seeders.builders.organization_builder import OrganizationBuilder
from seeders.framework.base import BaseSeeder
from seeders.user_seeder import UserSeeder


class OrganizationSeeder(BaseSeeder):
    """
    Seeds the default organization.
    """

    name = "organizations"

    depends_on = (
        UserSeeder,
    )

    async def run(self) -> None:
        builder = OrganizationBuilder(self.session)

        owner = self.context["owner"]

        organization = await builder.get_or_create(
            owner=owner,
            name="Test Organization",
            slug="test-organization",
            description="Total fresh-thinking model",
        )

        self.context["organization"] = organization