from __future__ import annotations

from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import AsyncSessionLocal
from repositories.chatbot_repository import ChatbotRepository
from repositories.chatbot_ai_config_repository import (
    ChatbotAIConfigRepository,
)
from repositories.invitation_repository import InvitationRepository
from repositories.member_repository import MemberRepository
from repositories.organization_repository import OrganizationRepository
from repositories.user_repository import UserRepository


class UnitOfWork:
    """
    Coordinates repositories and manages a single database transaction.
    """

    def __init__(self) -> None:
        self._session: AsyncSession | None = None

        self._users: UserRepository | None = None
        self._organizations: OrganizationRepository | None = None
        self._members: MemberRepository | None = None
        self._invitations: InvitationRepository | None = None
        self._chatbots: ChatbotRepository | None = None
        self._chatbot_ai_configs: (
            ChatbotAIConfigRepository | None
        ) = None

    @property
    def session(self) -> AsyncSession:
        """
        Return the active session.

        Raises:
            RuntimeError: if accessed before entering the context.
        """
        if self._session is None:
            raise RuntimeError(
                "UnitOfWork has not been entered."
            )

        return self._session

    async def __aenter__(self) -> UnitOfWork:
        self._session = AsyncSessionLocal()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        try:
            if exc_type is not None:
                await self.rollback()
        finally:
            await self.session.close()

            # Reset session
            self._session = None

            # Reset repositories
            self._users = None
            self._organizations = None
            self._members = None
            self._invitations = None
            self._chatbots = None
            self._chatbot_ai_configs = None

    # ---------------------------------------------------------
    # Transaction API
    # ---------------------------------------------------------

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def flush(self) -> None:
        await self.session.flush()

    async def refresh(
        self,
        instance: object,
    ) -> None:
        await self.session.refresh(instance)

    # ---------------------------------------------------------
    # Lazy repositories
    # ---------------------------------------------------------

    @property
    def users(self) -> UserRepository:
        if self._users is None:
            self._users = UserRepository(self.session)
        return self._users

    @property
    def organizations(self) -> OrganizationRepository:
        if self._organizations is None:
            self._organizations = OrganizationRepository(
                self.session
            )
        return self._organizations

    @property
    def members(self) -> MemberRepository:
        if self._members is None:
            self._members = MemberRepository(
                self.session
            )
        return self._members

    @property
    def invitations(self) -> InvitationRepository:
        if self._invitations is None:
            self._invitations = InvitationRepository(
                self.session
            )
        return self._invitations

    @property
    def chatbots(self) -> ChatbotRepository:
        if self._chatbots is None:
            self._chatbots = ChatbotRepository(
                self.session
            )
        return self._chatbots

    @property
    def chatbot_ai_configs(
        self,
    ) -> ChatbotAIConfigRepository:
        if self._chatbot_ai_configs is None:
            self._chatbot_ai_configs = (
                ChatbotAIConfigRepository(
                    self.session
                )
            )
        return self._chatbot_ai_configs