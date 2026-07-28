from tools.seed.user_seed import UserSeed
from seeders.builders.organization_builder import OrganizationBuilder

from tools.seed.base import BaseSeed


class OrganizationSeed(BaseSeed):
    """
    Seed the default organization.
    """

    name = "organizations"
    depends_on = [
        UserSeed,
        ]

    async def run(self) -> None:
        owner = self.context.get("owner")

        if owner is None:
            raise RuntimeError("Owner user not found in execution context.")

        builder = OrganizationBuilder(self.session)

        organization = await builder.get_or_create(
            owner=owner,
            slug="default-org",
            name="Default Organization",
            description="Default organization for development.",
        )

        self.context.set("organization", organization)