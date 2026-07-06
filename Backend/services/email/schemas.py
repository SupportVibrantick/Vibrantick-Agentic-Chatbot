from typing import Any

from pydantic import BaseModel, EmailStr, Field


class EmailRequest(BaseModel):
    """
    Generic email request used by every email provider.
    """

    subject: str = Field(..., min_length=1)

    recipients: list[EmailStr] = Field(..., min_length=1)

    template: str = Field(..., min_length=1)

    context: dict[str, Any] = Field(default_factory=dict)