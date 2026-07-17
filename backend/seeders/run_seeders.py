import asyncio

from database.engine import AsyncSessionLocal

from seeders.user_seeder import UserSeeder
from seeders.organization_seeder import OrganizationSeeder
from seeders.member_seeder import MemberSeeder
from seeders.invitation_seeder import InvitationSeeder


async def seed():
    async with AsyncSessionLocal() as session:

        user_seeder = UserSeeder(session)
        organization_seeder = OrganizationSeeder(session)
        member_seeder = MemberSeeder(session)
        invitation_seeder = InvitationSeeder(session)

        print("Creating users...")

        owner = await user_seeder.owner()
        admin = await user_seeder.admin()
        members = await user_seeder.create_many(5)

        print("Creating organization...")

        organization = await organization_seeder.get_or_create(
            owner=owner,
            name="Test Organization",
            slug="test-organization",
            description="Total fresh-thinking model",
            )

        print("Creating organization members...")

        await member_seeder.owner(
            organization=organization,
            user=owner,
        )

        await member_seeder.admin(
            organization=organization,
            user=admin,
        )

        await member_seeder.create_many(
            organization=organization,
            users=members,
        )

        print("Creating invitations...")

        await invitation_seeder.create(
            organization=organization,
            inviter=owner,
            email="pending1@test.com",
        )

        await invitation_seeder.create(
            organization=organization,
            inviter=owner,
            email="pending2@test.com",
        )

        print()
        print("=" * 50)
        print("✅ Database seeded successfully!")
        print("=" * 50)
        print(f"Organization : {organization.name}")
        print(f"Owner        : {owner.email}")
        print(f"Admin        : {admin.email}")
        print(f"Members      : {len(members)}")
        print("Invitations  : 2")
        print("=" * 50)


if __name__ == "__main__":
    asyncio.run(seed())