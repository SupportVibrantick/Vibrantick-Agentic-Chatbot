from __future__ import annotations

from faker import Faker
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import get_password_hash
from models.user import User


class UserBuilder:
    """
    Builder responsible for creating User entities.

    This class contains only entity creation logic and should never
    commit transactions. Transaction management is handled by the
    ExecutionManager.
    """

    DEFAULT_PASSWORD = "password123"

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.fake = Faker()

    async def create(
        self,
        full_name: str | None = None,
        email: str | None = None,
        password: str | None = None,
    ) -> User:
        """
        Create a single user.
        """

        password = password or self.DEFAULT_PASSWORD

        user = User(
            full_name=full_name or self.fake.name(),
            email=email or self.fake.unique.email(),
            hashed_password=get_password_hash(password),
        )

        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)

        return user

    async def create_many(
        self,
        count: int,
        password: str | None = None,
    ) -> list[User]:
        """
        Create multiple users.
        """

        users: list[User] = []

        for _ in range(count):
            users.append(
                await self.create(
                    password=password,
                )
            )

        return users

    async def get_or_create(
        self,
        email: str,
        full_name: str | None = None,
        password: str | None = None,
    ) -> User:
        """
        Return an existing user if one exists with the given email,
        otherwise create a new one.
        """

        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)

        user = result.scalar_one_or_none()

        if user is not None:
            return user

        return await self.create(
            full_name=full_name,
            email=email,
            password=password,
        )

    async def owner(self) -> User:
        """
        Return the default organization owner.
        """

        return await self.get_or_create(
            email="owner@test.com",
            full_name="Organization Owner",
        )

    async def admin(self) -> User:
        """
        Return the default system administrator.
        """

        return await self.get_or_create(
            email="admin@test.com",
            full_name="System Admin",
        )