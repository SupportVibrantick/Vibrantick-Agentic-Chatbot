from services.email.providers.base import BaseEmailProvider
from services.email.providers.smtp_provider import SMTPProvider
from services.email.schemas import EmailRequest


class EmailService:
    """
    High-level email service.

    The application interacts with this class instead of talking
    directly to SMTP, SES, or any other provider.
    """

    def __init__(
        self,
        provider: BaseEmailProvider | None = None,
    ):
        self.provider = provider or SMTPProvider()

    async def send_email(
        self,
        email: EmailRequest,
    ) -> None:
        await self.provider.send_email(email)