from __future__ import annotations

from seeders.builders.user_builder import UserBuilder
from seeders.framework.base import BaseSeeder


class UserSeeder(BaseSeeder):
    """
    Seeds the initial users required by the application.
    """

    name = "users"

    depends_on = ()

    async def run(self) -> None:
        builder = UserBuilder(self.session)

        owner = await builder.owner()
        admin = await builder.admin()
        members = await builder.create_many(5)

        self.context["owner"] = owner
        self.context["admin"] = admin
        self.context["members"] = members