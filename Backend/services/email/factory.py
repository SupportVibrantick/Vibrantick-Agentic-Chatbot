from services.email.providers.base import BaseEmailProvider
from services.email.providers.smtp_provider import SMTPProvider
from core.settings import settings


class EmailProviderFactory:
    """
    Creates the configured email provider.
    """

    @staticmethod
    def create() -> BaseEmailProvider:
        provider = settings.EMAIL_PROVIDER.lower()

        if provider == "smtp":
            return SMTPProvider()

        raise ValueError(
            f"Unsupported email provider: {provider}"
        )