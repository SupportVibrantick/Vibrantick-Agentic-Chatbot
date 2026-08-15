from __future__ import annotations

from seeders.builders.invitation_builder import InvitationBuilder
from seeders.base import BaseSeeder


class InvitationSeeder(BaseSeeder):
    """
    Seeds organization invitations.
    """

    name = "invitations"

    depends_on = (
        "users",
        "organizations",
        "organization_members",
    )

    async def run(self) -> None:
        builder = InvitationBuilder(self.session)

        organization = self.context["organization"]
        owner = self.context["owner"]

        invitations = await builder.create_many(
            organization=organization,
            inviter=owner,
            emails=[
                "john@example.com",
                "alice@example.com",
                "bob@example.com",
            ],
        )

        self.context["invitations"] = invitations