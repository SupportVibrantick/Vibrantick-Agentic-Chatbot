from seeders.builders.member_builder import MemberBuilder

from tools.seed.base import BaseSeed

from tools.seed.organization_seed import OrganizationSeed
class MemberSeed(BaseSeed):
    """
    Seed the default organization membership.
    """

    name = "members"
    depends_on = [
        OrganizationSeed,
    ]
    async def run(self) -> None:

        organization = self.context.get("organization")
        owner = self.context.get("owner")
        admin = self.context.get("admin")

        if organization is None:
            raise RuntimeError("Organization not found in execution context.")

        if owner is None:
            raise RuntimeError("Owner user not found in execution context.")

        if admin is None:
            raise RuntimeError("Admin user not found in execution context.")

        builder = MemberBuilder(self.session)

        owner_member = await builder.owner(
            organization=organization,
            user=owner,
        )

        admin_member = await builder.admin(
            organization=organization,
            user=admin,
        )

        self.context.set("owner_member", owner_member)
        self.context.set("admin_member", admin_member)