from core.jwt import create_access_token
from core.security import hash_password, verify_password
from database.unit_of_work import UnitOfWork
from models.user import User
from schemas.auth import UserRegister


class AuthService:
    """
    Handles authentication business logic.

    The service owns no database session.
    It operates through a UnitOfWork.
    """

    def __init__(
        self,
        uow: UnitOfWork,
    ) -> None:
        self.uow = uow

    async def register(
        self,
        user_data: UserRegister,
    ) -> User:

        existing_user = await self.uow.users.get_by_email(
            user_data.email
        )

        if existing_user:
            raise ValueError("Email already registered")

        user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            hashed_password=hash_password(
                user_data.password
            ),
        )

        await self.uow.users.add(user)

        await self.uow.flush()

        await self.uow.refresh(user)

        await self.uow.commit()

        return user

    async def authenticate(
        self,
        email: str,
        password: str,
    ) -> User | None:

        user = await self.uow.users.get_by_email(email)

        if user is None:
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

        if user is None:
            return None

        return create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
                "type": "access",
            }
        )