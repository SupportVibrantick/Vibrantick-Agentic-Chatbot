from sqlalchemy import Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.roles import OrganizationRole
from database.base import Base
from models.base import TimestampMixin


class OrganizationMember(TimestampMixin, Base):
    __tablename__ = "organization_members"

    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "user_id",
            name="uq_org_user",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    role: Mapped[OrganizationRole] = mapped_column(
        Enum(OrganizationRole),
        default=OrganizationRole.MEMBER,
        nullable=False,
    )

    organization = relationship(
        "Organization",
        back_populates="members",
    )

    user = relationship(
        "User",
        back_populates="organization_memberships",
    )