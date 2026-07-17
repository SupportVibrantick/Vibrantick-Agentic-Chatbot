from abc import ABC, abstractmethod

from services.email.schemas import EmailRequest


class BaseEmailProvider(ABC):
    """
    Base interface for all email providers.
    """

    @abstractmethod
    async def send_email(
        self,
        email: EmailRequest,
    ) -> None:
        """
        Send an email.

        Every provider (SMTP, SES, SendGrid, etc.)
        must implement this method.
        """
        raise NotImplementedError