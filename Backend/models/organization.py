from sqlalchemy import (
    String,
    Text,
    ForeignKey,
    UniqueConstraint,
    Enum,
)
from core.roles import OrganizationRole
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base
from models.base import TimestampMixin


class Organization(TimestampMixin, Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    slug: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    logo: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    owner = relationship(
    "User",
    foreign_keys=[owner_id],
    back_populates="organizations",
    )

    members = relationship(
        "OrganizationMember",
        back_populates="organization",
        cascade="all, delete-orphan",
    )
    
    
    
    invitations = relationship(
    "Invitation",
    back_populates="organization",
    cascade="all, delete-orphan",
)


class OrganizationMember(TimestampMixin, Base):
    __tablename__ = "organization_members"

    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "user_id",
            name="uq_org_user",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

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