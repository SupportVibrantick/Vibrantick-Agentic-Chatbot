from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict

from core.roles import (
    OrganizationRole,
    InvitationStatus,
)

class InvitationCreate(BaseModel):
    email: EmailStr
    role: OrganizationRole = OrganizationRole.MEMBER
    
class InvitationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    organization_id: int
    invited_by: int

    email: EmailStr

    role: OrganizationRole
    status: InvitationStatus

    expires_at: datetime
    accepted_at: datetime | None

    created_at: datetime
    updated_at: datetime
    
    
class InvitationListResponse(BaseModel):
    invitations: list[InvitationResponse]