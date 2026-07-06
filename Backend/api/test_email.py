from fastapi import APIRouter

from services.email.email_service import EmailService
from services.email.schemas import EmailRequest

router = APIRouter(
    prefix="/test",
    tags=["Email Test"],
)


@router.get("/email")
async def send_test_email():

    email = EmailRequest(
        subject="Vibrantic AI - Email Test",
        recipients=["YOUR_EMAIL@gmail.com"],  # Replace with your email
        template="emails/invitation.html",
        context={
            "organization_name": "Demo Workspace",
            "inviter_name": "Lovish",
            "invitation_link": "http://localhost:3000/invitation/test-token",
        },
    )

    service = EmailService()

    await service.send_email(email)

    return {"message": "Test email sent successfully."}