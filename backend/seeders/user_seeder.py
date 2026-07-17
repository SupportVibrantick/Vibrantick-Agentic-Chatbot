from faker import Faker

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import get_password_hash
from models.user import User
from seeders.base import BaseSeeder


fake = Faker()


class UserSeeder(BaseSeeder):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(
        self,
        full_name: str | None = None,
        email: str | None = None,
        password: str = "password123",
    ) -> User:

        user = User(
            full_name=full_name or fake.name(),
            email=email or fake.unique.email(),
            hashed_password=get_password_hash(password),
        )

        await self.add(user)
        await self.commit()
        await self.refresh(user)

        return user

    async def create_many(
        self,
        count: int,
        password: str = "password123",
    ) -> list[User]:

        users: list[User] = []

        for _ in range(count):
            user = User(
                full_name=fake.name(),
                email=fake.unique.email(),
                hashed_password=get_password_hash(password),
            )

            self.session.add(user)
            users.append(user)

        await self.commit()

        for user in users:
            await self.refresh(user)

        return users

    async def get_or_create(
        self,
        email: str,
        full_name: str | None = None,
        password: str = "password123",
    ) -> User:

        stmt = select(User).where(User.email == email)

        result = await self.session.execute(stmt)

        user = result.scalar_one_or_none()

        if user:
            return user

        return await self.create(
            full_name=full_name,
            email=email,
            password=password,
        )

    async def admin(self) -> User:
        return await self.get_or_create(
            email="admin@test.com",
            full_name="System Admin",
            password="password123",
        )

    async def owner(self) -> User:
        return await self.get_or_create(
            email="owner@test.com",
            full_name="Organization Owner",
            password="password123",
        )