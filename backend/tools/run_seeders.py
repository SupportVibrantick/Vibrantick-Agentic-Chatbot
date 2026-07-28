import asyncio

from database.session import AsyncSessionLocal

from tools.core.manager import ExecutionManager
from tools.core.registry import SeederRegistry

from backend.seeders.builders.user_builder import UserBuilder
from backend.seeders.builders.organization_seeder import OrganizationSeeder
from backend.seeders.builders.member_builder import MemberSeeder
from backend.seeders.builders.invitation_builder import InvitationSeeder


async def main():

    registry = SeederRegistry()

    registry.register(UserBuilder)
    registry.register(OrganizationSeeder)
    registry.register(MemberSeeder)
    registry.register(InvitationSeeder)

    manager = ExecutionManager(
        session_factory=AsyncSessionLocal,
        registry=registry,
    )

    await manager.execute()


if __name__ == "__main__":
    asyncio.run(main())