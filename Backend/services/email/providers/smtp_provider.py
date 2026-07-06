from fastapi_mail import FastMail, MessageSchema, MessageType

from core.email import mail_config
from services.email.providers.base import BaseEmailProvider
from services.email.schemas import EmailRequest


class SMTPProvider(BaseEmailProvider):
    """
    SMTP implementation of the BaseEmailProvider.
    """

    def __init__(self):
        self.client = FastMail(mail_config)

    async def send_email(
        self,
        email: EmailRequest,
    ) -> None:

        message = MessageSchema(
            subject=email.subject,
            recipients=email.recipients,
            template_body=email.context,
            subtype=MessageType.html,
        )

        await self.client.send_message(
            message,
            template_name=email.template,
        )