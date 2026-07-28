from seeders.builders.user_builder import UserBuilder

from tools.seed.base import BaseSeed


class UserSeed(BaseSeed):
    """
    Seeds the default system users.
    """

    name = "users"
    depends_on = []

    async def run(self) -> None:

        builder = UserBuilder(self.session)

        admin = await builder.admin()
        owner = await builder.owner()

        self.context.set("admin", admin)
        self.context.set("owner", owner)