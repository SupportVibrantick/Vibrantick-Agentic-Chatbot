from fastapi_mail import FastMail, MessageSchema, MessageType

from core.email import mail_config


class EmailService:

    @staticmethod
    async def send_invitation_email(
        recipient: str,
        organization_name: str,
        inviter_name: str,
        invitation_link: str,
    ):

        message = MessageSchema(
            subject=f"You're invited to join {organization_name}",
            recipients=[recipient],
            template_body={
                "organization_name": organization_name,
                "inviter_name": inviter_name,
                "invitation_link": invitation_link,
            },
            subtype=MessageType.html,
        )

        fm = FastMail(mail_config)

        await fm.send_message(
            message,
            template_name="invitation.html",
        )