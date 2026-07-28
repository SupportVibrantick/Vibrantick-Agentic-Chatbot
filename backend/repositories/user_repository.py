from sqlalchemy import select

from models.user import User
from repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    Repository responsible for User-specific queries.
    """

    model = User

    async def get_by_email(
        self,
        email: str,
    ) -> User | None:
        """
        Retrieve a user by email.
        """
        stmt = (
            select(User)
            .where(User.email == email)
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()