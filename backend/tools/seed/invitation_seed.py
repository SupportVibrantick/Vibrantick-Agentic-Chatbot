from seeders.builders.invitation_builder import InvitationBuilder

from tools.seed.base import BaseSeed

from tools.seed.member_seed import MemberSeed
class InvitationSeed(BaseSeed):
    """
    Seed the default organization invitations.
    """

    name = "invitations"
    depends_on = [
        MemberSeed,
    ]

    async def run(self) -> None:

        organization = self.context.get("organization")
        admin = self.context.get("admin")

        if organization is None:
            raise RuntimeError("Organization not found in execution context.")

        if admin is None:
            raise RuntimeError("Admin user not found in execution context.")

        builder = InvitationBuilder(self.session)

        invitation = await builder.get_or_create(
            organization=organization,
            inviter=admin,
            email="member@test.com",
        )

        self.context.set("invitation", invitation)