from __future__ import annotations

from seeders.builders.member_builder import MemberBuilder
from seeders.framework.base import BaseSeeder
from seeders.organization_seeder import OrganizationSeeder
from seeders.user_seeder import UserSeeder


class MemberSeeder(BaseSeeder):
    """
    Seeds organization memberships.
    """

    name = "organization_members"

    depends_on = (
        UserSeeder,
        OrganizationSeeder,
    )

    async def run(self) -> None:
        builder = MemberBuilder(self.session)

        organization = self.context["organization"]
        owner = self.context["owner"]
        admin = self.context["admin"]
        members = self.context["members"]

        await builder.owner(
            organization=organization,
            user=owner,
        )

        await builder.admin(
            organization=organization,
            user=admin,
        )

        await builder.create_many(
            organization=organization,
            users=members,
        ) 