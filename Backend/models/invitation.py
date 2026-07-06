from datetime import datetime
from sqlalchemy import (
    String,
    DateTime,
    ForeignKey,
    Enum,
    
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from database.base import Base
from models.base import TimestampMixin
from core.roles import (
    OrganizationRole,
    InvitationStatus,
)


class Invitation(TimestampMixin, Base):
    __tablename__ = "invitations"

  

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
    )

    invited_by: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    token: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False,
        index=True,
    )

    role: Mapped[OrganizationRole] = mapped_column(
    Enum(OrganizationRole),
    default=OrganizationRole.MEMBER,
    nullable=False,
    )

    status: Mapped[InvitationStatus] = mapped_column(
        Enum(InvitationStatus),
        default=InvitationStatus.PENDING,
        nullable=False,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    accepted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    organization = relationship(
        "Organization",
        back_populates="invitations",
    )

    inviter = relationship(
        "User",
        foreign_keys=[invited_by],
    )
from sqlalchemy import (
    String,
    DateTime,
    ForeignKey,
    Enum,
    
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from database.base import Base
from models.base import TimestampMixin
from core.roles import (
    OrganizationRole,
    InvitationStatus,
)

