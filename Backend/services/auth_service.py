from sqlalchemy.ext.asyncio import AsyncSession

from core.jwt import create_access_token
from core.security import hash_password, verify_password
from models.user import User
from repositories.user_repository import UserRepository
from schemas.auth import UserRegister


class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repository = UserRepository(db)

    async def register(self, user_data: UserRegister) -> User:

        existing_user = await self.user_repository.get_by_email(
            user_data.email
        )

        if existing_user:
            raise ValueError("Email already registered")

        hashed_password = hash_password(user_data.password)

        user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            hashed_password=hashed_password,
        )

        return await self.user_repository.create(user)

    async def authenticate(
        self,
        email: str,
        password: str,
    ) -> User | None:

        user = await self.user_repository.get_by_email(email)

        if not user:
            return None

        if not verify_password(
            password,
            user.hashed_password,
        ):
            return None

        return user

    async def login(
        self,
        email: str,
        password: str,
    ) -> str | None:

        user = await self.authenticate(
            email,
            password,
        )

        if not user:
            return None

        token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
                "type": "access",
            }
        )

        return token