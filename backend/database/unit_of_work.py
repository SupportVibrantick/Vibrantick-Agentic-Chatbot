
from __future__ import annotations

from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import AsyncSessionLocal

from repositories.user_repository import UserRepository
from repositories.organization_repository import OrganizationRepository
from repositories.member_repository import MemberRepository
from repositories.invitation_repository import InvitationRepository
from repositories.chatbot_repository import ChatbotRepository
from repositories.chatbot_ai_config_repository import (
    ChatbotAIConfigRepository,
)
from repositories.knowledge_base_repository import (
    KnowledgeBaseRepository,
)
from repositories.document_repository import (
    DocumentRepository,
)
from repositories.document_chunk_repository import (
    DocumentChunkRepository,
)
from repositories.conversation_repository import ConversationRepository
from repositories.message_repository import MessageRepository


class UnitOfWork:
    """
    Coordinates repositories and manages a single database transaction.

    A UnitOfWork can either:
    - create its own AsyncSession for normal application usage, or
    - receive an existing AsyncSession for tests / externally managed
      transactions.
    """

    def __init__(
        self,
        session: AsyncSession | None = None,
    ) -> None:
        self._session = session
        self._external_session = session is not None

        self._users: UserRepository | None = None
        self._organizations: OrganizationRepository | None = None
        self._members: MemberRepository | None = None
        self._invitations: InvitationRepository | None = None
        self._chatbots: ChatbotRepository | None = None
        self._chatbot_ai_configs: (
            ChatbotAIConfigRepository | None
        ) = None
        self._knowledge_bases: (
            KnowledgeBaseRepository | None
        ) = None
        self._documents: (
            DocumentRepository | None
        ) = None
        self._document_chunks: (
            DocumentChunkRepository | None
        ) = None
        self._conversations: ConversationRepository | None = None
        self._messages: MessageRepository | None = None

    # ---------------------------------------------------------
    # Session
    # ---------------------------------------------------------

    @property
    def session(self) -> AsyncSession:
        if self._session is None:
            raise RuntimeError(
                "UnitOfWork has not been entered."
            )

        return self._session

    async def __aenter__(self) -> UnitOfWork:
        if self._session is None:
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
            if not self._external_session:
                await self.session.close()

            self._session = None

            self._users = None
            self._organizations = None
            self._members = None
            self._invitations = None
            self._chatbots = None
            self._chatbot_ai_configs = None
            self._knowledge_bases = None
            self._documents = None
            self._document_chunks = None
            self._conversations = None
            self._messages = None

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

    @property
    def knowledge_bases(
        self,
    ) -> KnowledgeBaseRepository:
        if self._knowledge_bases is None:
            self._knowledge_bases = (
                KnowledgeBaseRepository(
                    self.session
                )
            )

        return self._knowledge_bases

    @property
    def documents(
        self,
    ) -> DocumentRepository:
        if self._documents is None:
            self._documents = (
                DocumentRepository(
                    self.session
                )
            )

        return self._documents

    @property
    def document_chunks(
        self,
    ) -> DocumentChunkRepository:
        if self._document_chunks is None:
            self._document_chunks = (
                DocumentChunkRepository(
                    self.session
                )
            )

        return self._document_chunks

    @property
    def conversations(self) -> ConversationRepository:
        if self._conversations is None:
            self._conversations = ConversationRepository(self.session)
        return self._conversations

    @property
    def messages(self) -> MessageRepository:
        if self._messages is None:
            self._messages = MessageRepository(self.session)
        return self._messages
