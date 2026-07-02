from pydantic import BaseModel, EmailStr

from core.roles import OrganizationRole


class MemberCreate(BaseModel):
    email: EmailStr
    role: OrganizationRole = OrganizationRole.MEMBER


class MemberUpdateRole(BaseModel):
    role: OrganizationRole


class MemberResponse(BaseModel):
    id: int
    organization_id: int
    user_id: int
    role: str

    model_config = {
        "from_attributes": True
    }