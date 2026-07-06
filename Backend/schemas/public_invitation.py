from datetime import datetime

from pydantic import BaseModel


class PublicInvitationResponse(BaseModel):
    organization_name: str
    email: str
    role: str
    expires_at: datetime